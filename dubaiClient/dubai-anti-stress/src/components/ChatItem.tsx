import React from 'react';
import type { Chat } from '../types/chat';

interface ChatItemProps {
  chat: Chat;
  onClick: () => void;
}

const ChatItem: React.FC<ChatItemProps> = ({ chat, onClick }) => {
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) {
      return 'Just now';
    } else if (diffInHours < 24) {
      return `${diffInHours}h ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  return (
    <div 
      className="flex items-center gap-3 p-4 hover:bg-gray-50 cursor-pointer transition-colors border-b border-bayut-border last:border-b-0"
      onClick={onClick}
    >
      <div className="w-12 h-12 bg-bayut-primary rounded-full flex items-center justify-center text-white font-medium flex-shrink-0">
        {chat.title.split(' ')[0][0]}{chat.title.split(' ')[1][0]}
      </div>
      
      <div className="flex-1 min-w-0">
        <div className="flex justify-between items-start mb-1">
          <h4 className="font-semibold text-bayut-dark text-sm truncate">
            {chat.title}
          </h4>
          <span className="text-xs text-bayut-gray ml-2 flex-shrink-0">
            {formatTime(chat.lastMessage?.timestamp || chat.createdAt)}
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          <p className="text-sm text-bayut-gray truncate">
            {chat.lastMessage?.text || 'No messages yet'}
          </p>
          {chat.unreadCount > 0 && (
            <span className="w-5 h-5 bg-bayut-primary text-white text-xs rounded-full flex items-center justify-center flex-shrink-0">
              {chat.unreadCount}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatItem;