import type { Chat, ChatMessage } from '../types/chat';

export const mockChats: Chat[] = [
  {
    id: '1',
    title: 'John Smith - Property Inquiry',
    participants: ['user1', 'user2'],
    lastMessage: {
      id: '1',
      senderId: 'user2',
      recipientId: 'user1',
      text: 'Hi!  interested in the apartment in Downtown Dubai. Is it still available?',
      timestamp: '2024-01-15T14:30:00Z',
      isRead: false
    },
    unreadCount: 1,
    createdAt: '2024-01-15T14:00:00Z'
  },
  {
    id: '2',
    title: 'Sarah Johnson - Villa Inquiry',
    participants: ['user1', 'user3'],
    lastMessage: {
      id: '2',
      senderId: 'user1',
      recipientId: 'user3',
      text: 'The villa looks great! Can we schedule a viewing this weekend?',
      timestamp: '2024-01-14T16:45:00Z',
      isRead: true
    },
    unreadCount: 0,
    createdAt: '2024-01-14T16:00:00Z'
  },
  {
    id: '3',
    title: 'Michael Brown - Studio Inquiry',
    participants: ['user1', 'user4'],
    lastMessage: {
      id: '3',
      senderId: 'user4',
      recipientId: 'user1',
      text: 'Is the studio furnished? What included in the price?',
      timestamp: '2024-01-13T10:15:00Z',
      isRead: true
    },
    unreadCount: 0,
    createdAt: '2024-01-13T10:00:00Z'
  }
];

export const mockMessages: ChatMessage[] = [
  {
    id: '1',
    senderId: 'user2',
    recipientId: 'user1',
    text: 'Hi! I interested in the apartment in Downtown Dubai. Is it still available?',
    timestamp: '2024-01-15T14:30:00Z',
    isRead: false
  },
  {
    id: '2',
    senderId: 'user1',
    recipientId: 'user2',
    text: 'Yes, it still available! Would you like to schedule a viewing?',
    timestamp: '2024-01-15T14:35:00Z',
    isRead: true
  },
  {
    id: '3',
    senderId: 'user3',
    recipientId: 'user1',
    text: 'The villa looks great! Can we schedule a viewing this weekend?',
    timestamp: '2024-01-14T16:45:00Z',
    isRead: true
  },
  {
    id: '4',
    senderId: 'user1',
    recipientId: 'user3',
    text: 'Sure! How about Saturday at 2 PM?',
    timestamp: '2024-01-14T16:50:00Z',
    isRead: true
  },
  {
    id: '5',
    senderId: 'user4',
    recipientId: 'user1',
    text: 'Is the studio furnished? What included in the price?',
    timestamp: '2024-01-13T10:15:00Z',
    isRead: true
  },
  {
    id: '6',
    senderId: 'user1',
    recipientId: 'user4',
    text: 'Yes, it fully furnished with modern appliances. The price includes utilities.',
    timestamp: '2024-01-13T10:20:00Z',
    isRead: true
  }
];