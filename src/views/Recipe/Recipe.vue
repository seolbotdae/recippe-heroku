<template>
  <v-container>
    레시피 기본화면
    <v-data-table
      :headers="headers"
      :items="recipes"
      :items-per-page="3"
      class="elevation-1"
    ></v-data-table>
    <v-btn to="/recipe/create">작성하기</v-btn>
    <v-text-field v-model="recipeID" label="레시피 게시글 열람 테스트용"></v-text-field>
    <v-btn @click="toLookup(recipeID)">아이디 전달</v-btn>
    <v-btn @click="searchRecipeList">레시피 검색</v-btn>
    <v-btn @click="sortRecipeList">레시피 정렬</v-btn>
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';

export default {
  data () {
    return {
      headers: [
        { text: 'id', value: 'post_id' },
        { text: 'title', value: 'title' },
        { text: 'nickname', value: 'nickname' },
        { text: 'spicy', value: 'degree_of_spicy' },
        { text: 'like', value: 'like_count' },
        { text: 'comment', value: 'comment_count' },
        { text: 'view', value: 'views' },
        { text: 'time', value: 'upload_time' },
      ],
      recipes: [],
      recipeID: null,
      total_page: null
    }
  },
  mounted() {
    let vm = this;
    herokuAPI.recipeList(1)
      .then(function(response) {
        console.log("리스트 응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            for(let i = 0; response.data.recipeList[i] != null; i++) {
              vm.recipes.push(response.data.recipeList[i]);
            }
            tp = response.data.total_page;
          }
      })
  },
  methods: {
    toLookup(recipeID) {
      router.push({
        path: "/recipe/lookup/"+recipeID,
      })
    },
    searchRecipeList() {
      let list = [];
      let tp;
      const searchInfo = JSON.stringify({
        "searchType": "카테고리",
        "categories": "test0-test2",
        "keywordType": null,
        "keyword": null,
        "page": 1
      });
      herokuAPI.recipeSearch(searchInfo)
        .then(function(response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
              console.log("검색 성공");
              for(let i = 0; response.data.recipeList[i] != null; i++) {
                list.push(response.data.recipeList[i]);
              }
              tp = response.data.total_page;
            }
        })
      this.recipes = list;
      this.total_page = tp;
    },
    sortRecipeList() {
      let list = [];
      const sortInfo = JSON.stringify({
        "arrangeBy": "좋아요 순",
        "page": 1
      });
      herokuAPI.recipeSort(sortInfo)
        .then(function (response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
            console.log("정렬 성공");
            for(let i = 0; response.data[i] != null; i++) {
              list.push(response.data[i]);
            }
          }
        })
      this.recipes = list;
    }
  }
}
</script>