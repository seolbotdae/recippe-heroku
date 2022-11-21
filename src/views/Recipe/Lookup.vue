<template>
  <v-container>
    <v-row>
      <v-col>
        lookup page
        <div> {{ requestRecipe }} </div>
        <v-btn @click="deleteRecipe" style="width: 100%">게시글 삭제</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';

export default {
  data () {
    return {
      requestRecipe: null
    }
  },
  async mounted() {
    let pid = this.$route.params.id;
    console.log("post_id", pid);
    if(pid == null) {
      console.log("ERROR");
    }
    let vm = this;
    herokuAPI.recipeLookup(pid)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            vm.requestRecipe = response.data;
          }
      })
  },
  methods: {
    deleteRecipe() {
      const deleteTarget = JSON.stringify({ requestRecipe });
      herokuAPI.recipeDelete(deleteTarget)
        .then(function (response){
          if(response.status == 200) {
            console.log("삭제 성공");
          }
        }) 
    },
    
  }
}
</script>