import axios from 'axios';

export {
    OpalAPI
};

function OpalAPI() {

    // Request on OIDC
    this.getAccessToken = function(config, code){
        const url = config.token_uri;
        const token = btoa(config.client_id+":"+config.client_secret);
        const redirect_uri = config.redirect_uri;

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

    // Request on OIDC
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

    // Request on OIDC
    this.getUserInfo = function(){
        const url = '/user_info/';
        return axios.request({
          url: url,
          method:'get',
          headers: {
              'Content-Type':'application/json',
          }
        }).then(response => response.data);
    }

    // Request on OIDC
    this.redirectForLogin = function(config, callback_url){
        if(config && config.auth_uri){
            var q = new URLSearchParams();
            q.set('client_id', config.client_id);
            q.set('redirect_uri', callback_url);
            q.set('scope', config.scopes);
            q.set('response_type','code');
            q.set('openid.realm', callback_url);
            window.location = config.auth_uri +"?"+ q.toString();
        }else{
            return false;
        }
    }

    // Request on Opal Data Provider
    this.getOpalResourceList = function(opal_dp_url, resource_name){
        const url = '/'+resource_name+'/';
        return axios.request({
          url: url,
          method:'get',
          baseURL: opal_dp_url,
          headers: {
              'Content-Type':'application/json'
          }
        }).then(response => response.data);
    }

    // Request on Opal Data Provider
    this.getOpalResourceInfo = function(opal_dp_url, resource_name, id){
        const url = '/'+resource_name+'/'+id;
        return axios.request({
          url: url,
          method:'get',
          baseURL: opal_dp_url,
          headers: {
              'Content-Type':'application/json'
          }
        }).then(response => response.data);
    }

    // Request on Opal Client
    this.registerClient = function(client){
        const url = '/client/';
        return axios.request({
            url: url,
            method:'post',
            headers: {
                'Content-Type':'application/json',
            },
            data: client,
        }).then(response => response.data);
    }

    // Request on Opal Client
    this.getClientList = function(){
        const url = '/client/';
        return axios.request({
            url: url,
            method:'get',
            headers: {
                'Content-Type':'application/json',
            },
        }).then(response => response.data);
    }

    // Request on Opal Client
    this.getClient = function(id){
        const url = '/client/'+id;
        return axios.request({
            url: url,
            method:'get',
            headers: {
                'Content-Type':'application/json',
            },
        }).then(response => response.data);
    }

    // Request on Opal Client
    this.getTokenInfo = function(){
        const url = '/token_info/';
        return axios.request({
            url: url,
            method:'get',
            headers: {
                'Content-Type':'application/json'
            },
        }).then(response => response.data);
    }
}
