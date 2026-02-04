import React, { useState, useEffect } from 'react';
import { Notification } from '../types/notification';
import { mockNotifications } from '../mock/notificationMock';
import NotificationItem from './NotificationItem';

interface NotificationListProps {
  onNotificationSelect: (notification: Notification) => void;
}

const NotificationList: React.FC<NotificationListProps> = ({ onNotificationSelect }) = > {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() = > {
    // Имитация загрузки данных
    const timer = setTimeout(() = > {
      setNotifications(mockNotifications);
      setLoading(false);
    }, 500);
    return () = > clearTimeout(timer);
  }, []);

  const handleNotificationClick = (notification: Notification) = > {
    onNotificationSelect(notification);
  };

  if (loading) {
    return (
      <div className="flex justify-center py-16">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-bayut-primary"></div>
      </div>
    );
  }

  if (notifications.length === 0) {
    return (
      <div className="text-center py-8 px-4">
        <div className="text-bayut-gray mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-bayut-gray mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-bayut-dark mb-2">No Notifications</h3>
        <p className="text-sm text-bayut-gray">You have no new notifications</p>
      </div>
    );
  }

  return (
    <div className="space-y-2 overflow-y-auto max-h-[calc(100vh-200px)]">
      {notifications.map((notification) = > (
        <NotificationItem
          key={notification.id}
          notification={notification}
          onClick={() = > handleNotificationClick(notification)}
        />
      ))}
    </div>
  );
};

export default NotificationList;