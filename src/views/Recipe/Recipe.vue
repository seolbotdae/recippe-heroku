<template>
  <v-container>
    레시피 기본화면
    <v-data-table
      :headers="headers"
      :items="recipes"
      :items-per-page="5"
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
        {
          text: 'Dessert (100g serving)',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        { text: 'Calories', value: 'calories' },
        { text: 'Fat (g)', value: 'fat' },
        { text: 'Carbs (g)', value: 'carbs' },
        { text: 'Protein (g)', value: 'protein' },
        { text: 'Iron (%)', value: 'iron' },
      ],
      recipes: []
    }
  },
  mounted() {
    herokuAPI.recipeList(1)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            recipes = response.data;
            console.log(recipes);
          }
      })
  },
  methods: {

  }
}
</script>