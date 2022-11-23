import axios from "axios";

const BASE_URL = "https://recippe-sg.herokuapp.com/"

export default {
  /* Authentication */
  login: function(User) {
    return axios.post(BASE_URL+'login/', User);
  },
  firstcheck: function(info) {
    return axios.post(BASE_URL+'firstcheck/', info);
  },
  secondcheck: function(info) {
    return axios.post(BASE_URL+'secondcheck/', info);
  },
  signup: function(info) {
    return axios.post(BASE_URL+'signup/', info);
  },
  changeNN: function(info) {
    return axios.post(BASE_URL+'changenickname/', info);
  },
  changePW: function(info) {
    return axios.post(BASE_URL+'changepw/', info);
  },

  /* MyPage */
  refrigeratorLookup: function(nickname) {
    return axios.get(BASE_URL+'inquiryrefrigerator/'+nickname+'/');
  },
  refrigeratorDelete: function(info) {
    return axios.post(BASE_URL+'deleterefrigerator/', info);
  },
  refrigeratorEdit: function(info) {
    return axios.post(BASE_URL+'updaterefrigerator/', info);
  },
  myphotosLookup: function(nickname) {
    return axios.get(BASE_URL+'inquirymyphotoposts/'+nickname+'/');
  },
  myrecipesLookup: function(nickname) {
    return axios.get(BASE_URL+'inquirymyrecipeposts/'+nickname+'/');
  },
  myrecipesSearch: function(info) {
    return axios.post(BASE_URL+'querymyrecipeposts/', info);
  },
  myrecipesSort: function(info) {
    return axios.post(BASE_URL+'arrangemyrecipeposts/', info);
  },
  mylikeposts: function(nickname, postType) {
    return axios.get(BASE_URL+'inquirymylikeposts/'+nickname+'/'+postType+'/');
  },
  mycommentposts: function(nickname) {
    return axios.get(BASE_URL+'inquirymycommentposts/'+nickname+'/');
  },

  /* RecipePost */
  recipeList: function(page) {
    return axios.get(BASE_URL+'recipeboard/'+page+'/');
  },
  recipeLookup: function(post_id, nickname) {
    return axios.get(BASE_URL+'recipe/'+post_id+'/'+nickname+'/');
  },
  recipeAdd: function(info) {
    return axios.post(BASE_URL+'uploadrecipe/', info);
  },
  recipeEdit: function(info) {
    return axios.post(BASE_URL+'updaterecipe/', info);
  },
  recipeDelete: function(info) {
    return axios.post(BASE_URL+'deleterecipe/', info);
  },
  recipeLike: function(info) {
    return axios.post(BASE_URL+'likerecipe/', info);
  },
  recipeUnLike: function(info) {
    return axios.post(BASE_URL+'likerecipe/', info);
  },
  recipeSearch: function(info) {
    return axios.post(BASE_URL+'queryrecipe/', info);
  },
  recipeSort: function(info) {
    return axios.post(BASE_URL+'sortrecipe/', info);
  },
  recipeReport: function(info) {
    return axios.post(BASE_URL+'reportrecipe/', info);
  },
  unExistIntredients: function(nickname, post_id) {
    return axios.get(BASE_URL+'unexistingredients/'+nickname+'/'+post_id+'/');
  },
  decreaseAmount: function(nickname, post_id) {
    return axios.get(BASE_URL+'decreaseamount/'+nickname+'/'+post_id+'/')
  },

  /* PhotoPost */
  photoList: function(page) {
    return axios.get(BASE_URL+'photoboard/'+page+'/');
  },
  photoLookup: function(post_id, nickname) {
    return axios.get(BASE_URL+'photo/'+post_id+'/'+nickname+'/');
  },
  photoAdd: function(info) {
    return axios.post(BASE_URL+'uploadphoto/', info);
  },
  photoDelete: function(info) {
    return axios.delete(BASE_URL+'deletephoto/', {
      data : info
    });
  },
  photoSort: function(info) {
    return axios.post(BASE_URL+'sortphoto/', info);
  },
  photoLike: function(info) {
    return axios.post(BASE_URL+'likephoto/', info);
  },
  photoUnLike: function(info) {
    return axios.post(BASE_URL+'likephoto/', info);
  },
  photoReport: function(info) {
    return axios.post(BASE_URL+'reportphoto/', info);
  },

  /* Mail */
  mailList: function(nickname, page) {
    return axios.get(BASE_URL+'inquiremaillist/'+nickname+'/'+page+'/');
  },
  mailLookup: function(mail_id) {
    return axios.get(BASE_URL+'inquiremail/'+mail_id+'/');
  },
  mailSend: function(info) {
    return axios.post(BASE_URL+'insertmail/', info);
  },
  mailDelete: function(info) {
    return axios.post(BASE_URL+'deletemail/', info);
  }
}