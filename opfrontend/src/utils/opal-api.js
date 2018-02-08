import axios from 'axios';

export {
  OpalAPI
};

function OpalAPI(BASE_URL) {

    this.test = function(msg){
      console.log(BASE_URL, msg);
    }
    
    this.getUserInfo = function(token){
      const url = '/api/userinfo';
      return axios.request({
          url: url,
          method:'get',
          baseURL: BASE_URL,
          headers: {
              'Content-Type':'application/json',
              'Authorization': `Bearer ${token}`
          }
      }).then(response => response.data);
  }
}
