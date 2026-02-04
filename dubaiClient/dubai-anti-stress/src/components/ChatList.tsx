import React, { useState, useEffect } from 'react';
import type { Chat, ChatMessage } from '../types/chat';
import { mockChats, mockMessages } from '../mock/chatMock';
import ChatItem from './ChatItem';

interface ChatListProps {
  onChatSelect: (chat: Chat) => void;
}

const ChatList: React.FC<ChatListProps> = ({ onChatSelect }) => {
  const [chats, setChats] = useState<Chat[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Simulate loading data
    const timer = setTimeout(() => {
      setChats(mockChats);
      setLoading(false);
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  const handleChatClick = (chat: Chat) => {
    onChatSelect(chat);
  };

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-bayut-primary"></div>
      </div>
    );
  }

  if (chats.length === 0) {
    return (
      <div className="text-center py-8 px-4">
        <div className="text-bayut-gray mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-bayut-gray mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-bayut-dark mb-2">No Chats Yet</h3>
        <p className="text-sm text-bayut-gray">Start a conversation with property owners</p>
      </div>
    );
  }

  return (
    <div className="space-y-2 overflow-y-auto max-h-[calc(100vh-200px)]">
      {chats.map((chat) => (
        <ChatItem
          key={chat.id}
          chat={chat}
          onClick={() => handleChatClick(chat)}
        />
      ))}
    </div>
  );
};

export default ChatList;