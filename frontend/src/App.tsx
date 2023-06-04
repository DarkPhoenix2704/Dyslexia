import { useEffect, useState } from "react";
import { fakerEN_US } from "@faker-js/faker";
import { AudioRecorder, useAudioRecorder } from "react-audio-voice-recorder";

function App() {
  const [words, setWords] = useState<string[]>([]);
  const [seconds, setSeconds] = useState<number>(0);

  const [blob, setBlob] = useState<Blob>();
  const controller = useAudioRecorder();

  const [isDyslexic, setIsDyslexic] = useState<boolean | null>(null);
  const [inAccuracy, setInAccuracy] = useState<number | null>(null);

  useEffect(() => {
    const words = fakerEN_US.word.words(10).split(" ");
    setWords(words);
  }, []);

  const stopRecording = () => {
    setSeconds(controller.recordingTime);
    controller.stopRecording();
  };

  const sendAudio = async () => {
    const formData = new FormData();
    formData.append("file", blob as Blob);
    formData.append("seconds", seconds.toString());
    formData.append("string_displayed", words.join(" "));
    const response = await fetch("http://localhost:5000", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    setIsDyslexic(data.isDyslexic);
    setInAccuracy(data.pronounciation_inaccuracy);
  };

  return (
    <div className="flex flex-col h-[100vh] items-center justify-center gap-2 bg-[#141414] text-white">
      <h1 className="text-5xl font-semibold">LexiScan</h1>
      <h1 className="text-xl text-center">
        Dyslexia Diagnosis using Machine Learning
      </h1>
      <div className="flex flex-wrap items-center justify-center gap-1 mt-4">
        {words.map((word, index) => (
          <span
            key={index}
            className="px-3 text-lg py-1 bg-[#1f1f1f] rounded-md "
          >
            {word}
          </span>
        ))}
      </div>
      <AudioRecorder
        onRecordingComplete={async (blob: Blob) => {
          setBlob(blob);
          await sendAudio();
        }}
        recorderControls={controller}
        audioTrackConstraints={{
          noiseSuppression: true,
          echoCancellation: true,
        }}
      />
      <button
        className="px-4 py-2 bg-[#1f1f1f] rounded-md"
        onClick={stopRecording}
      >
        Stop Recording
      </button>
      <div className="flex flex-col items-center justify-center gap-2">
        <h1
          className={`text-xl text-center font-semibold ${
            isDyslexic ? "text-red-600" : "text-green-400"
          }`}
        >
          {isDyslexic === null}
          {isDyslexic === true && "You are Dyslexic"}
          {isDyslexic === false && "You are not Dyslexic"}
          <br />
          {inAccuracy && `Pronounciation Inaccuracy: ${inAccuracy * 100}%`}
        </h1>
      </div>
    </div>
  );
}

export default App;
