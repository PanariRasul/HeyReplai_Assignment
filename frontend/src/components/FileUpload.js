import React, { useState } from 'react';
import axios from 'axios';

function FileUpload({ setVadResults }) {
    const [file, setFile] = useState(null);
    const [error, setError] = useState('');

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) {
            setError('Please upload an audio file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(process.env.REACT_APP_API_URL, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setVadResults(response.data.vad_results);
        } catch (error) {
            setError('Error uploading the file. Please try again.');
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} accept=".wav" />
                <button type="submit">Upload</button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}

export default FileUpload;
