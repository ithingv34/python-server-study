import React from "react";
import ReactDOM from 'react-dom/client';
import { ChakraProvider } from "@chakra-ui/react";

import Header from "./components/Header";
import Todos from "./components/Todos";

function App() {
  return (
    <ChakraProvider>
      <Header />
      <Todos />
    </ChakraProvider>
  )
}

const rootElement = document.getElementById("root")
ReactDOM.createRoot(rootElement).render(<App />, )


