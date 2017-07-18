import axios from 'axios';

class TabletopApi {

    constructor() {
        this.httpClient = axios.create({
            baseURL: 'http://localhost:5000/api/',
            timeout: 10000,
            withCredentials: true,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
    }

    search(query) {
        return this.httpClient.get(`search?q=${query}`)
    }
}

export default TabletopApi;
