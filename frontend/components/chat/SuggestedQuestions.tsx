import { Button } from "@/components/ui/button";

const questions = [
  "Should I invest in Infosys?",
  "Compare Infosys and TCS",
  "Latest news about Reliance",
  "IT sector outlook",
];

interface Props {
  onSelect: (question: string) => void;
}

export default function SuggestedQuestions({ onSelect }: Props) {
  return (
    <div className="mb-8">
      <h2 className="mb-4 text-sm font-medium text-slate-400">
        Suggested Questions
      </h2>

      <div className="flex flex-wrap gap-3">
        {questions.map((question) => (
          <Button
            key={question}
            variant="outline"
            className="rounded-full"
            onClick={() => onSelect(question)}
          >
            {question}
          </Button>
        ))}
      </div>
    </div>
  );
}