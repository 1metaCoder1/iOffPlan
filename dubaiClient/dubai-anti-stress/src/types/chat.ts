export interface ChatMessage {
  id: string;
  senderId: string;
  recipientId: string;
  text: string;
  timestamp: string;
  isRead: boolean;
}

export interface Chat {
  id: string;
  title: string;
  participants: string[];
  lastMessage?: ChatMessage;
  unreadCount: number;
  createdAt: string;
}

export interface ChatUser {
  id: string;
  name: string;
  avatar?: string;
  role: 'buyer' | 'seller';
}

export interface ChatState {
  chats: Chat[];
  currentChat?: Chat;
  messages: ChatMessage[];
  loading: boolean;
  error?: string;
}