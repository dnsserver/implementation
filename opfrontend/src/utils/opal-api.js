import axios from 'axios';

export {
    OpalAPI
};

function OpalAPI() {

    this.getAccessToken = function(config, code){
        const url = config.token_uri;
        const token = btoa(config.client_id+":"+config.client_secret);
        const redirect_uri = config.base_url+config.redirect_uri;

        var params = new URLSearchParams();
        params.append('grant_type', 'authorization_code');
        params.append('code', code);
        params.append('redirect_uri', redirect_uri);
        return axios.request({
            url: url,
            method:'post',
            headers: {
                'Content-Type':'application/x-www-form-urlencoded',
                'Authorization': `Basic ${token}`
            },
            data: params,
        }).then(response => response.data);
    }

    this.getWellKnownURLs = function(base_url){
        const url = '/.well-known/openid-configuration';
        return axios.request({
          url: url,
          method:'get',
          baseURL: base_url,
          headers: {
              'Content-Type':'application/json',
          }
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

    this.getOpalResourceList = function(base_url, resource_name){
        const url = '/'+resource_name+'/';
        return axios.request({
          url: url,
          method:'get',
          baseURL: base_url,
          headers: {
              'Content-Type':'application/json'
          }
        }).then(response => response.data);
    }

    this.getOpalResourceInfo = function(base_url, resource_name, id){
        const url = '/'+resource_name+'/'+id;
        return axios.request({
          url: url,
          method:'get',
          baseURL: base_url,
          headers: {
              'Content-Type':'application/json'
          }
        }).then(response => response.data);
    }

    this.registerClient = function(base_url, token, client){
        const url = '/client/';

        return axios.request({
            url: url,
            method:'post',
            baseURL: base_url,
            headers: {
                'Content-Type':'application/json',
                'Authorization': `Bearer ${token}`
            },
            data: client,
        }).then(response => response.data);
    }
}
