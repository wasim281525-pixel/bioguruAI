'use client';
import { useState, useRef } from 'react';
import { authHeaders } from '@/lib/api';

export function useVoice() {
  const [recording, setRecording] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  const mediaRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      recorder.ondataavailable = e => chunksRef.current.push(e.data);
      recorder.start();
      mediaRef.current = recorder;
      setRecording(true);
    } catch {
      alert('Microphone access denied.');
    }
  };

  const stopRecording = (): Promise<string> => {
    return new Promise(resolve => {
      if (!mediaRef.current) { resolve(''); return; }
      mediaRef.current.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setTranscribing(true);
        try {
          const form = new FormData();
          form.append('audio', blob, 'recording.webm');
          form.append('language', 'auto');
          const res = await fetch('/api/voice/transcribe', {
            method: 'POST',
            headers: authHeaders(),
            body: form,
          });
          const data = await res.json();
          resolve(data.transcript || '');
        } catch {
          resolve('');
        } finally {
          setTranscribing(false);
        }
      };
      mediaRef.current.stop();
      mediaRef.current.stream.getTracks().forEach(t => t.stop());
      setRecording(false);
    });
  };

  return { recording, transcribing, startRecording, stopRecording };
}
