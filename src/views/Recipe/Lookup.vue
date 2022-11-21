<template>
  <v-container>
    <v-row>
      <v-col>
        lookup page
        <div> {{ requestRecipe }} </div>
        <v-btn @click="deleteRecipe" style="width: 100%">게시글 삭제</v-btn>
        <v-btn @click="likeRecipe('등록')" style="width: 100%">좋아요 등록</v-btn>
        <v-btn @click="likeRecipe('취소')" style="width: 100%">좋아요 삭제</v-btn>
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
  mounted() {
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
    likeRecipe(task) {
      let like_task = task;
      const likeInfo = JSON.stringify({
        "like_id": 0,
        "nickname": "test",
        "postType": 1,
        "postId": 28,
        "task": like_task
      });
      if(like_task === '등록') {
        herokuAPI.recipeLike(likeInfo)
        .then(function (response) {
          if(response.status == 200) {
            console.log("좋아요 등록 성공");
          }
        })
      } else {
        herokuAPI.recipeUnLike(likeInfo)
          .then(function (response) {
            if(response.status == 200) {
              console.log("좋아요 취소 성공");
            }
          })
      }
    }
  }
}
</script>