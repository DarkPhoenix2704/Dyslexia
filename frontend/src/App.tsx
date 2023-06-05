function App() {
  return (
    <div className="flex flex-col h-[100vh] items-center justify-center gap-2 bg-[#141414] text-white">
      <h1 className="text-5xl font-semibold">LexiScan</h1>
      <h1 className="text-xl text-center">
        Dyslexia Diagnosis using Machine Learning
      </h1>
      <div className="flex flex-row items-center justify-center gap-2">
        <button className="px-3 py-2 bg-[#1f1f1f] rounded-md">
          <a href="/voice">Dyslexia Detection Using Voice</a>
        </button>
        <button className="px-3 py-2 bg-[#1f1f1f] rounded-md">
          <a href="/image">Dyslexia Detection Using HandWriting</a>
        </button>
      </div>
    </div>
  );
}

export default App;
