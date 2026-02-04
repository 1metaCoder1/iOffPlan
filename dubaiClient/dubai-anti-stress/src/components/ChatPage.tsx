import React, { useState, useEffect } from 'react';
import type { Chat, ChatMessage } from '../types/chat';
import { mockMessages } from '../mock/chatMock';

interface ChatPageProps {
  chat: Chat;
}

const ChatPage: React.FC<ChatPageProps> = ({ chat }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Фильтруем сообщения для текущего чата
    const filteredMessages = mockMessages.filter(
      (msg) => msg.senderId === chat.participants[1] || msg.recipientId === chat.participants[1]
    );
    
    const timer = setTimeout(() => {
      setMessages(filteredMessages);
      setLoading(false);
    }, 500);
    
    return () => clearTimeout(timer);
  }, [chat]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputMessage.trim()) {
      // Здесь должна быть логика отправки сообщения
      console.log('Sending message: ', inputMessage);
      setInputMessage('');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-bayut-primary"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <header className="bg-white border-b border-bayut-border px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button
            onClick={() => console.log('Go back to chat list')}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-bayut-primary rounded-full flex items-center justify-center text-white font-medium">
              {chat.title.split(' ')[0][0]}{chat.title.split(' ')[1][0]}
            </div>
            <div>
              <h4 className="font-semibold text-bayut-dark text-sm">{chat.title}</h4>
              <span className="text-xs text-bayut-gray">Online</span>
            </div>
          </div>
        </div>
        <button className="p-2 rounded-lg hover:bg-gray-100 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </button>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto px-4 py-6">
        {messages.length === 0 ? (
          <div className="text-center text-bayut-gray">
            <div className="text-4xl mb-4"><svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg></div>
            <h4 className="font-medium text-bayut-dark mb-2">No messages yet</h4>
            <p className="text-sm text-bayut-gray">Start the conversation by sending a message</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={message.id}
              className={`mb-4 ${message.senderId === chat.participants[1] ? 'text-right' : 'text-left'}`}
            >
              <div
                className={`inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.senderId === chat.participants[1]
                    ? 'bg-bayut-primary text-white'
                    : 'bg-gray-100 text-bayut-dark'
                }`}
              >
                <p className="text-sm">{message.text}</p>
                <span className="text-xs text-bayut-gray block mt-1">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))
        )}
      </main>

      {/* Input */}
      <footer className="bg-white border-t border-bayut-border px-4 py-3">
        <form onSubmit={handleSendMessage} className="flex items-center gap-3">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 px-4 py-2 border border-bayut-border rounded-lg focus:outline-none focus:ring-2 focus:ring-bayut-primary"
          />
          <button
            type="submit"
            disabled={!inputMessage.trim()}
            className="p-2 rounded-lg hover:bg-bayut-primary hover:text-white transition-colors disabled:opacity-50"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </form>
      </footer>
    </div>
  );
};

export default ChatPage;