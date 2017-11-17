import axios from 'axios';

const BASE_URL = "http://localhost:5000";
export default class Service {
    sendTrainingData(data){
        return axios.post(BASE_URL+'/save', {data: data});
    }
    getPrediction(data){
        return axios.post(BASE_URL+'/predict', {data: data});
    }
}
