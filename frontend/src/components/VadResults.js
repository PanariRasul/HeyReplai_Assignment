import React from 'react';

function VadResults({ vadResults }) {
    if (!vadResults.length) return null;

    return (
        <div>
            <h2>VAD Results</h2>
            <ul>
                {vadResults.map((result, index) => (
                    <li key={index}>
                        {`Time: ${result.time.toFixed(2)}s - Speech Detected: ${result.is_speech}`}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default VadResults;
