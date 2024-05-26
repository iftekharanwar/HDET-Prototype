import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, Button, Input, FormControl, FormLabel, Table, Thead, Tbody, Tr, Th, Td, Alert, AlertIcon } from '@chakra-ui/react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setErrorMessage('');
    setSuccessMessage('');
  };

  const handleImport = async () => {
    if (file) {
      const fileType = file.name.split('.').pop().toLowerCase();
      if (fileType !== 'xlsx' && fileType !== 'xml') {
        setErrorMessage('Unsupported file type. Please upload an Excel (.xlsx) or XML (.xml) file.');
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post('https://hsi-data-app-yq6johqe.devinapps.com/import', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log(response.data);
        setSuccessMessage('Data imported successfully!');
        // Fetch the updated data from the backend
        fetchData();
      } catch (error) {
        console.error('Error importing data:', error);
        setErrorMessage('Error importing data. Please try again.');
      }
    }
  };

  const fetchData = async () => {
    try {
      const response = await axios.get('https://hsi-data-app-yq6johqe.devinapps.com/export');
      console.log('Fetched data:', response.data); // Log the fetched data
      setData(response.data);
      console.log('Updated state data:', response.data); // Log the updated state
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // Use useEffect to fetch data when the component mounts
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <ChakraProvider>
      <Box p={4}>
        <FormControl>
          <FormLabel>Import Hardware Data (Supported file types: .xlsx, .xml)</FormLabel>
          <Input type="file" onChange={handleFileChange} />
          <Button mt={2} onClick={handleImport}>Import</Button>
        </FormControl>
        {errorMessage && (
          <Alert status="error" mt={4}>
            <AlertIcon />
            {errorMessage}
          </Alert>
        )}
        {successMessage && (
          <Alert status="success" mt={4}>
            <AlertIcon />
            {successMessage}
          </Alert>
        )}
        <Table mt={4}>
          <Thead>
            <Tr>
              <Th>ID</Th>
              <Th>IP Address</Th>
              <Th>DHCP Options</Th>
            </Tr>
          </Thead>
          <Tbody>
            {data.map((item) => (
              <Tr key={item.id}>
                <Td>{item.id}</Td>
                <Td>{item.ip_address}</Td>
                <Td>{item.dhcp_options}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    </ChakraProvider>
  );
}

export default App;
