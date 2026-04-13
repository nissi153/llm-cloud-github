import "./App.css";

function App() {
  return (
    // p-2 : padding 2만큼 준다.  마진: m-2
    // px- : padding x축              mx-
    // py- :  y축                     my-
    // pt- :  top                     mt-
    // pb- :  bottom                  mb-
    // pl- :  left                    ml-
    // pr- :  right                   mr-
    <>
      <div className="border-2 border-black p-8 m-4">박스1</div>
      <div className="border-2 border-black py-20 mt-20">박스2</div>
      <div className="border-2 border-black w-50 h-50">박스3</div>
      <div className="border-2 border-black text-red-500 bg-sky-300">박스4</div>
    </>
  );
}

export default App;
