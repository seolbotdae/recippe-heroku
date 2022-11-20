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
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';

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
      recipes: []
    }
  },
  mounted() {
    let list = null;
    herokuAPI.recipeList(1)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            list = response.data.recipeList;
          }
      })
      for(let i = 0; list[i] != null; i++) {
        this.recipes.push(list[i]);
        console.log(this.recipes);
      }
  },
  methods: {

  }
}
</script>