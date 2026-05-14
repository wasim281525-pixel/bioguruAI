'use client';
import { useVoice } from '@/hooks/useVoice';
import { Mic, MicOff, Loader2 } from 'lucide-react';

interface Props {
  onTranscript: (text: string) => void;
}

export function VoiceRecorder({ onTranscript }: Props) {
  const { recording, transcribing, startRecording, stopRecording } = useVoice();

  const handleClick = async () => {
    if (recording) {
      const text = await stopRecording();
      if (text) onTranscript(text);
    } else {
      await startRecording();
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={transcribing}
      title={recording ? 'Stop recording' : 'Start voice input'}
      className={`p-2 rounded-lg transition ${
        recording
          ? 'bg-red-100 text-red-600 animate-pulse'
          : transcribing
          ? 'bg-gray-100 text-gray-400'
          : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
      }`}
    >
      {transcribing ? (
        <Loader2 size={18} className="animate-spin" />
      ) : recording ? (
        <MicOff size={18} />
      ) : (
        <Mic size={18} />
      )}
    </button>
  );
}
