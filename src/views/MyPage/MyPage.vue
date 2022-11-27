<template>
  <v-container>
    <v-layout>
      <v-col offset="1" cols="10">
        <v-card color="#f5efe6" class="py-2">
          <v-card-title class="pl-10 my-text">나의 활동</v-card-title>
          <v-card-actions class="pl-15">
            <v-btn text to="/mypage/myphoto" color="#7895B2">내가 올린 사진</v-btn>
            <v-btn text to="/mypage/likedphoto" color="#7895B2">좋아요 누른 사진</v-btn>
          </v-card-actions>
          <v-card-actions class="pl-15">
            <v-btn text to="/mypage/myrecipe" color="#7895B2">내가 쓴 레시피</v-btn>
            <v-btn text to="/mypage/likedrecipe" color="#7895B2">좋아요 누른 레시피</v-btn>
          </v-card-actions>
          <v-card-actions class="pl-15">
            <v-btn text to="/mypage/commentrecipe" color="#7895B2">댓글 단 레시피</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-layout>

    <v-layout>
      <v-col offset="1" cols="5">
        <v-card color="#f5efe6" class="py-2">
          <v-card-title class="pl-10 my-text">냉장고</v-card-title>
          <v-card-actions class="pl-15">
            <v-btn text @click="requestRefri()" color="#7895B2">냉장고 조회</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>


      <v-col cols="5">
        <v-card color="#f5efe6" class="py-2">
          <v-card-title class="pl-10 my-text">쪽지함</v-card-title>
          <v-card-actions class="pl-15">
            <v-btn text @click="requestML()" color="#7895B2">쪽지 조회</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      
    </v-layout>

    <v-layout>
      <v-col offset="1" cols="10" class="py-2">
        <v-card color="#f5efe6" class="py-2">
          <v-card-title class="ml-10 my-text">계정 관리</v-card-title>
          <v-card-actions class="ml-15">
            <v-btn text @click="changeNi()" color="#7895B2">닉네임 변경</v-btn>
          </v-card-actions>
          <v-card-actions class="ml-15">
            <v-btn text @click="changePW()" color="#7895B2">비밀번호 변경</v-btn>
          </v-card-actions>
          
        </v-card>
      </v-col>
    </v-layout>


    <!-- <v-btn @click="changePW">비밀번호 변경</v-btn> -->
  </v-container>
</template>

<style>
.my-text{
  color: #7895B2;
}

</style>

<script>
import router from '@/router/index.js';
import herokuAPI from '@/api/heroku.js';

export default {
  data() {
    return {
      myphotos: [],
      myrecipes: [],
    };
  },
  methods: {
    changePW() {
      router.push({
        path: "/email-auth/1",
      })
    },
    changeNi() {
      router.push({
        path: "/mypage/changeNickname",
      })
    },
    requestML() {
      router.push({
        path: "/mail"
      })
    },
    requestRefri() {
      router.push({
        path: "/mypage/refrigerator",
      })
    },
    lookupMyLikeList() { // 좋아요 누른 게시글
      let vm = this;
      let postType = 1; /* 1=레시피, -1=사진 */
      const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
      herokuAPI.mylikeposts(UserInfo.nickname, postType)
        .then(function(response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
            console.log("조회 성공");
            if(postType == 1) for(let i = 0; response.data[i] != null; i++) vm.myrecipes.push(response.data[i]);
            else for(let i = 0; response.data[i] != null; i++) vm.myphotos.push(response.data[i]);
          }
        })
    },
  }
}
</script>