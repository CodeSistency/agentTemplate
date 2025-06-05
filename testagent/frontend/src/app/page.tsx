"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat, useCopilotChat } from "@copilotkit/react-ui";
import { useCallback, useEffect, useRef, useState } from "react";
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import "@copilotkit/react-ui/styles.css";

// Custom message component to render markdown with math support
function MessageContent({ content }: { content: string }) {
  const html = marked.parse(content || '');
  const safeHtml = DOMPurify.sanitize(html);
  
  return (
    <div 
      className="prose max-w-none"
      dangerouslySetInnerHTML={{ __html: safeHtml }}
    />
  );
}

// Custom chat component to handle message rendering
export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);
  
  useEffect(() => {
    scrollToBottom();
  }, [scrollToBottom]);

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <div className="container mx-auto">
          <h1 className="text-2xl font-bold">Math Tutor AI</h1>
          <p className="text-sm opacity-80">Your personal AI math assistant</p>
        </div>
      </header>
      
      <main className="flex-1 overflow-hidden flex flex-col">
        <CopilotKit runtimeUrl="http://localhost:8080/copilotkit">
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            <CopilotChat
              labels={{
                title: "Math Tutor",
                initial: [
                  "# Welcome to Math Tutor AI! 🤖",
                  "I can help you with various math problems including:",
                  "- Basic arithmetic (+, -, ×, ÷)",
                  "- Exponents and roots",
                  "- Solving equations",
                  "- And more!",
                  "",
                  "Try asking me something like:",
                  "- "What is 123 × 456?"",
                  "- "Solve for x: 2x + 5 = 15"",
                  "- "What is the square root of 144?"",
                  "- "Calculate (5 + 3) × 2 - 10 ÷ 2""
                ].join("\n"),
              }}
              className="h-full"
              messageOptions={{
                className: "bg-white rounded-lg shadow p-4 my-2",
                loading: () => <div className="animate-pulse">Thinking...</div>,
                // @ts-ignore - The CopilotKit types don't include the content property
                component: ({ content }) => <MessageContent content={content} />
              }}
              onStateChange={({ status }) => {
                setIsLoading(status === 'streaming');
                if (status === 'done') {
                  setTimeout(scrollToBottom, 100);
                }
              }}
            />
            <div ref={messagesEndRef} />
          </div>
          
          {/* Status indicator */}
          <div className={`px-4 py-2 text-sm text-gray-500 bg-gray-50 border-t ${isLoading ? 'animate-pulse' : ''}`}>
            {isLoading ? 'Math Tutor is thinking...' : 'Ask me a math question!'}
          </div>
        </CopilotKit>
      </main>
      
      <footer className="bg-gray-100 border-t p-2 text-center text-xs text-gray-500">
        <p>Math Tutor AI © {new Date().getFullYear()} | Powered by AI</p>
      </footer>
    </div>
  );
}
