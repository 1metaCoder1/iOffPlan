import React, { useState } from 'react';
import type { Chat } from '../types/chat';
import { mockChats } from '../mock/chatMock';
import ChatList from '../components/ChatList';
import ChatPage from '../components/ChatPage';

interface ChatsPageProps {
  onChatSelect: (chat: Chat) => void;
}

const ChatsPage: React.FC<ChatsPageProps> = ({ onChatSelect }) => {
  const [currentChat, setCurrentChat] = useState<Chat | null>(null);

  const handleChatSelect = (chat: Chat) => {
    setCurrentChat(chat);
    onChatSelect(chat);
  };

  const handleBackToChatList = () => {
    setCurrentChat(null);
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <header className="bg-white border-b border-bayut-border px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="font-bold text-bayut-dark">
            Chats
          </div>
          {currentChat && (
            <button
              onClick={handleBackToChatList}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
          )}
        </div>
        <button className="p-2 rounded-lg hover:bg-gray-100 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </button>
      </header>

      {/* Content */}
      <main className="flex-1 overflow-hidden">
        {currentChat ? (
          <ChatPage chat={currentChat} />
        ) : (
          <ChatList onChatSelect={handleChatSelect} />
        )}
      </main>
    </div>
  );
};

export default ChatsPage;