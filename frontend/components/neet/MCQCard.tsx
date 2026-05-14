'use client';

interface Props {
  index: number;
  question: string;
  options: string[];
  selectedAnswer?: string;
  correctAnswer?: string;
  showResult?: boolean;
  onAnswer: (answer: string) => void;
}

export function MCQCard({ index, question, options, selectedAnswer, correctAnswer, showResult, onAnswer }: Props) {
  const getOptionClass = (opt: string) => {
    const letter = opt[0]; // 'A', 'B', 'C', 'D'
    if (!showResult) {
      return selectedAnswer === letter
        ? 'border-green-600 bg-green-50 text-green-800'
        : 'border-gray-200 hover:border-green-400 hover:bg-green-50 cursor-pointer';
    }
    if (letter === correctAnswer) return 'border-green-600 bg-green-50 text-green-800';
    if (letter === selectedAnswer && letter !== correctAnswer) return 'border-red-500 bg-red-50 text-red-700';
    return 'border-gray-200 text-gray-400';
  };

  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm">
      <div className="flex gap-2 mb-3">
        <span className="flex-shrink-0 w-7 h-7 rounded-full bg-green-700 text-white text-xs flex items-center justify-center font-bold">
          {index + 1}
        </span>
        <p className="text-sm font-medium text-gray-800 leading-relaxed">{question}</p>
      </div>
      <div className="space-y-2">
        {options.map(opt => {
          const letter = opt[0];
          return (
            <button
              key={letter}
              onClick={() => !showResult && onAnswer(letter)}
              disabled={showResult}
              className={`w-full text-left text-sm px-4 py-2.5 rounded-xl border-2 transition ${getOptionClass(opt)}`}
            >
              {opt}
            </button>
          );
        })}
      </div>
    </div>
  );
}
