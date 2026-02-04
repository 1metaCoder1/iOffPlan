import type { Notification } from '../types/notification';

export const mockNotifications: Notification[] = [
  {
    id: '1',
    title: 'System Update',
    message: 'The system will be temporarily unavailable for maintenance on February 5th from 2:00 AM to 4:00 AM UTC.',
    type: 'system',
    timestamp: '2024-02-04T10:00:00Z',
    isRead: false,
    data: {
      maintenance: {
        startTime: '2024-02-05T02:00:00Z',
        endTime: '2024-02-05T04:00:00Z',
        reason: 'System upgrade and performance improvements'
      }
    }
  },
  {
    id: '2',
    title: 'Document Processing Complete',
    message: 'Your property documents for listing ID #12345 have been successfully processed and verified.',
    type: 'important',
    timestamp: '2024-02-03T15:30:00Z',
    isRead: true,
    data: {
      listingId: '12345',
      status: 'verified',
      documents: ['passport_copy.pdf', 'title_deed.pdf', 'emirates_id.pdf']
    }
  },
  {
    id: '3',
    title: 'New Message Received',
    message: 'You have a new message from John Smith regarding your listing in Downtown Dubai.',
    type: 'info',
    timestamp: '2024-02-03T14:45:00Z',
    isRead: false,
    data: {
      chatId: '1',
      sender: 'John Smith',
      listing: 'Downtown Dubai Apartment'
    }
  },
  {
    id: '4',
    title: 'Server Maintenance Completed',
    message: 'The scheduled server maintenance has been completed successfully. All systems are now operational.',
    type: 'system',
    timestamp: '2024-01-30T04:15:00Z',
    isRead: true,
    data: {
      maintenanceId: 'maint_20240130',
      status: 'completed',
      improvements: ['Database optimization', 'Security patches', 'Performance improvements']
    }
  },
  {
    id: '5',
    title: 'Payment Confirmation',
    message: 'Your payment for premium listing has been successfully processed. Your listing is now featured.',
    type: 'important',
    timestamp: '2024-02-02T09:20:00Z',
    isRead: true,
    data: {
      transactionId: 'txn_98765',
      amount: 500,
      currency: 'AED',
      listingId: '12345',
      featureDuration: '30 days'
    }
  },
  {
    id: '6',
    title: 'New Property Listed',
    message: 'A new property matching your preferences has been listed in Dubai Marina.',
    type: 'info',
    timestamp: '2024-02-01T18:30:00Z',
    isRead: false,
    data: {
      propertyId: '8',
      location: 'Dubai Marina',
      price: 2500000,
      type: 'apartment'
    }
  },
  {
    id: '7',
    title: 'Account Verification Required',
    message: 'Please complete your account verification to access all platform features.',
    type: 'important',
    timestamp: '2024-01-28T11:15:00Z',
    isRead: false,
    data: {
      verificationSteps: [
        'Upload government ID',
        'Verify phone number',
        'Complete profile information'
      ],
      completionPercentage: 60
    }
  },
  {
    id: '8',
    title: 'System Performance Update',
    message: 'We have improved search performance by 40%. Property searches are now faster and more accurate.',
    type: 'system',
    timestamp: '2024-01-25T16:45:00Z',
    isRead: true,
    data: {
      improvements: [
        'Search response time reduced from 2s to 1.2s',
        'Image loading optimized by 30%',
        'Mobile app performance enhanced'
      ]
    }
  }
];