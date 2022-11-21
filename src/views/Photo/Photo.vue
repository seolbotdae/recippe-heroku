<template>
  <v-container>
    요리사진게시판 기본화면
    <v-btn to="/photo/create">작성하기</v-btn>
    <v-text-field v-model="photoID" label="사진 게시글 열람 테스트용"></v-text-field>
    <v-btn @click="toLookup(photoID)">아이디 전달</v-btn>
    <div>{{ photo }}</div>
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';

export default {
  data () {
    return {
      photo: [],
      photoID: null
    }
  },
  mounted() {
    let vm = this;
    herokuAPI.photoList(1)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            for(let i = 0; response.data.photoList[i] != null; i++) {
              vm.photo.push(response.data.photoList[i]);
            }
          }
      })
  },
  methods: {
    toLookup(photoID) {
      router.push({
        path: "/photo/lookup/"+photoID,
      })
    }
  }
}
</script>