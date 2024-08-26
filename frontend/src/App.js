import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import VadResults from './components/VadResults';

function App() {
    const [vadResults, setVadResults] = useState([]);

    return (
        <div className="App">
            <h1>Voice Activity Detection</h1>
            <FileUpload setVadResults={setVadResults} />
            <VadResults vadResults={vadResults} />
        </div>
    );
}

export default App;
