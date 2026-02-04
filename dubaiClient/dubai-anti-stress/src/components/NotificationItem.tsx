import React from 'react';
import { Notification } from '../types/notification';

interface NotificationItemProps {
  notification: Notification;
  onClick: () => void;
}

const NotificationItem: React.FC<NotificationItemProps> = ({ notification, onClick }) = > {
  const isUnread = !notification.isRead;
  const typeInfo = {
    system: { color: 'blue', icon: '<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd"/></svg>' },
    important: { color: 'orange', icon: '<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/></svg>' },
    info: { color: 'green', icon: '<svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/></svg>' }
  };

  return (
    <div
      onClick={onClick}
      className="cursor-pointer p-4 border-b border-bayut-border hover:bg-gray-50 transition-colors"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
              <div dangerouslySetInnerHTML={{ __html: typeInfo[notification.type].icon }} />
            </div>
            <div>
              <h4 className="font-semibold text-bayut-dark text-sm">{notification.title}</h4>
              <span className="text-xs text-bayut-gray">{notification.timestamp}</span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <p className="text-sm text-bayut-gray line-clamp-2">{notification.message}</p>
            </div>
            {isUnread && (
              <div className="bg-bayut-primary text-white text-xs font-medium px-2 py-1 rounded-full">
                New
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotificationItem;