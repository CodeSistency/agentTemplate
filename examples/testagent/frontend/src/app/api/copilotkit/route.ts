import { NextRequest } from 'next/server';

// This is a simple proxy to our Python backend
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8080';

export async function POST(req: NextRequest) {
  try {
    const url = new URL('/copilotkit', PYTHON_BACKEND_URL).toString();
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(await req.json()),
    });

    return new Response(response.body, {
      status: response.status,
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  } catch (error) {
    console.error('Error forwarding request to Python backend:', error);
    return new Response(JSON.stringify({ error: 'Failed to connect to backend service' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
