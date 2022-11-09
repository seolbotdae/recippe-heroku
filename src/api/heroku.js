import axios from "axios";

const BASE_URL = "https://recippe-sg.herokuapp.com/"

export default {
  login: function(User) {
    return axios.post(BASE_URL+'login/', User);
  },
  firstcheck: function(info) {
    return axios.post(BASE_URL+'firstcheck/', info)
  }
}