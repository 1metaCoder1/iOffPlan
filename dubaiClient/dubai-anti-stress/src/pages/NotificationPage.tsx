import React, { useState } from 'react'
import { useSelector } from 'react-redux'
import type { RootState } from '../store'
import type { Notification } from '../types/notification'
import { mockNotifications } from '../mock/notificationMock'

const NotificationPage: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>(mockNotifications)
  const [filter, setFilter] = useState<'all' | 'system' | 'important' | 'info'>('all')

  const filteredNotifications = notifications.filter(notification => {
    if (filter === 'all') return true
    return notification.type === filter
  })

  const markAsRead = (id: string) => {
    setNotifications(prev =>
      prev.map(notification =>
        notification.id === id
          ? { ...notification, isRead: true }
          : notification
      )
    )
  }

  const markAllAsRead = () => {
    setNotifications(prev =>
      prev.map(notification =>
        !notification.isRead
          ? { ...notification, isRead: true }
          : notification
      )
    )
  }

  const getNotificationIcon = (type: Notification['type']) => {
    switch (type) {
      case 'system':
        return (
          <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
        )
      case 'important':
        return (
          <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        )
      case 'info':
        return (
          <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        )
      default:
        return (
          <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </div>
        )
    }
  }

  const getNotificationColor = (type: Notification['type']) => {
    switch (type) {
      case 'system':
        return 'border-l-red-500'
      case 'important':
        return 'border-l-orange-500'
      case 'info':
        return 'border-l-blue-500'
      default:
        return 'border-l-gray-500'
    }
  }

  const unreadCount = notifications.filter(n => !n.isRead).length

  return (
    <div className="min-h-screen bg-bayut-light">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-3xl font-bold text-bayut-dark">Notifications</h1>
              <p className="text-bayut-gray mt-2">Stay updated with your account activity</p>
            </div>
            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                className="btn btn-primary text-sm"
              >
                Mark all as read
              </button>
            )}
          </div>

          <div className="flex gap-2 mb-6">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === 'all'
                  ? 'bg-bayut-primary text-white'
                  : 'bg-white text-bayut-gray hover:bg-gray-50'
              }`}
            >
              All ({notifications.length})
            </button>
            <button
              onClick={() => setFilter('system')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === 'system'
                  ? 'bg-red-500 text-white'
                  : 'bg-white text-bayut-gray hover:bg-gray-50'
              }`}
            >
              System ({notifications.filter(n => n.type === 'system').length})
            </button>
            <button
              onClick={() => setFilter('important')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === 'important'
                  ? 'bg-orange-500 text-white'
                  : 'bg-white text-bayut-gray hover:bg-gray-50'
              }`}
            >
              Important ({notifications.filter(n => n.type === 'important').length})
            </button>
            <button
              onClick={() => setFilter('info')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === 'info'
                  ? 'bg-blue-500 text-white'
                  : 'bg-white text-bayut-gray hover:bg-gray-50'
              }`}
            >
              Info ({notifications.filter(n => n.type === 'info').length})
            </button>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-bayut-border">
          {filteredNotifications.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-bayut-dark mb-2">No notifications</h3>
              <p className="text-bayut-gray">You're all caught up! No new notifications.</p>
            </div>
          ) : (
            <div className="divide-y divide-bayut-border">
              {filteredNotifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`p-6 hover:bg-gray-50 transition-colors ${getNotificationColor(notification.type)} ${!notification.isRead ? 'bg-blue-50/30' : ''}`}
                >
                  <div className="flex items-start gap-4">
                    {getNotificationIcon(notification.type)}
                    <div className="flex-1">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className={`font-medium ${!notification.isRead ? 'text-bayut-dark' : 'text-bayut-gray'}`}>
                          {notification.title}
                        </h3>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-bayut-gray">
                            {new Date(notification.timestamp).toLocaleDateString()}
                          </span>
                          {!notification.isRead && (
                            <span className="w-2 h-2 bg-bayut-primary rounded-full"></span>
                          )}
                        </div>
                      </div>
                      <p className={`text-sm mb-3 ${!notification.isRead ? 'text-bayut-gray' : 'text-bayut-gray/70'}`}>
                        {notification.message}
                      </p>
                      <div className="flex justify-between items-center">
                        <div className="flex gap-2">
                          <span className={`text-xs px-2 py-1 rounded-full ${
                            notification.type === 'system' ? 'bg-red-100 text-red-700' :
                            notification.type === 'important' ? 'bg-orange-100 text-orange-700' :
                            notification.type === 'info' ? 'bg-blue-100 text-blue-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {notification.type === 'system' ? 'System' :
                             notification.type === 'important' ? 'Important' :
                             notification.type === 'info' ? 'Info' : 'General'}
                          </span>
                        </div>
                        {!notification.isRead && (
                          <button
                            onClick={() => markAsRead(notification.id)}
                            className="text-xs text-bayut-primary hover:text-bayut-primary/80"
                          >
                            Mark as read
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default NotificationPage