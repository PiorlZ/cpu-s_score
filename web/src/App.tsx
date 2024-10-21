import React from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import { ProcTable } from './components/ProcTable';
import { useEffect, useState } from 'react';


const App = () => {
  const [tableData, setTableData] = useState([]);

  function getData(){
    axios({
      method: "POST",
      url: "http://127.0.0.1:5000/get_processor_data",
    })
    .then((response) => {
      setTableData(response.data);
      console.log(response.data)
    })
    .catch((error) => {
      console.log(error)
    })
  };

  useEffect(() => {
    getData();
  }, []);


  return (
    <div className="app-container">
      <ProcTable tableData={tableData}/>
    </div>
  );
}

export default App;
