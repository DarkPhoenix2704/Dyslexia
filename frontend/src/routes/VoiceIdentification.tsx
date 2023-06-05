import { useEffect, useState } from "react";
import { fakerEN_US } from "@faker-js/faker";
import { AudioRecorder, useAudioRecorder } from "react-audio-voice-recorder";

export const VoiceIdentification = () => {
  const [words, setWords] = useState<string[]>([]);
  const [seconds, setSeconds] = useState<number>(0);

  const [blob, setBlob] = useState<Blob>();
  const controller = useAudioRecorder();

  const [isDyslexic, setIsDyslexic] = useState<boolean | null>(null);
  // const [inAccuracy, setInAccuracy] = useState<number | null>(null);

  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    const words = fakerEN_US.word.words(10).split(" ");
    setWords(words);
  }, []);

  const stopRecording = () => {
    setSeconds(controller.recordingTime);
    controller.stopRecording();
  };

  const sendAudio = async () => {
    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", blob as Blob);
    formData.append("seconds", seconds.toString());
    formData.append("string_displayed", words.join(" "));
    fetch("http://localhost:5000", {
      method: "POST",
      body: formData,
    }).then((res) => {
      res
        .json()
        .then((data) => {
          setIsDyslexic(data.isDyslexic);
          // setInAccuracy(data.pronounciation_inaccuracy);
        })
        .finally(() => {
          setIsLoading(false);
        });
    });
  };

  return (
    <div className="flex flex-col h-[100vh] items-center justify-center gap-2 bg-[#141414] text-white">
      <h1 className="text-5xl text-center">
        Dyslexia Diagnosis using Machine Learning (Voice)
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
        className="px-4 py-2 bg-[#1f1f1f] flex flex-row items-center justify-center gap-2 rounded-md"
        onClick={stopRecording}
      >
        {isLoading ? (
          <svg
            className="animate-spin h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        ) : (
          <></>
        )}
        {isLoading ? "Loading..." : "Stop Recording"}
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
        </h1>
      </div>
    </div>
  );
};
