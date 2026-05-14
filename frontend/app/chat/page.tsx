'use client';
import AppLayout from '@/components/common/AppLayout';
import { ChatWindow } from '@/components/chat/ChatWindow';

export default function ChatPage() {
  return (
    <AppLayout>
      <div className="flex-1 overflow-hidden">
        <ChatWindow />
      </div>
    </AppLayout>
  );
}
