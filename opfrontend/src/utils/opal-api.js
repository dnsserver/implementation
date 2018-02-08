import axios from 'axios';

export {
    OpalAPI
};

function OpalAPI() {

    this.getAccessToken = function(config, code){
        const url = config.token_uri;
        //const token = btoa(config.client_id+":"+config.client_secret);
        const redirect_uri = config.base_url+config.redirect_uri;
        var q = new URLSearchParams();
        q.set('grant_type','authorization_code');
        q.set('code', code);
        q.set('redirect_uri', redirect_uri);

        return axios.request({
            url: url +"?"+q.toString(),
            method:'get',
            headers: {
                'Content-Type': 'text/plain'
            },
            auth: {
                username: config.client_id,
                password: config.client_secret
            },
        }).then(response => response.data);
    }

    this.getUserInfo = function(base_url, token){
        const url = '/api/userinfo';
        return axios.request({
          url: url,
          method:'get',
          baseURL: base_url,
          headers: {
              'Content-Type':'application/json',
              'Authorization': `Bearer ${token}`
          }
        }).then(response => response.data);
    }
}
