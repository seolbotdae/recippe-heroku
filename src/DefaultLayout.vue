<template>
  <v-card class="overflow-hidden">
    <v-app-bar
      color="#f5efe6"
      app dense fixed
    >

      <!-- 윗단 -->
      <v-col offset="2" cols="8">
        <div style="width:100%" class="d-flex justify-space-between align-center">
          <v-img
            contain
            max-width="40"
            src="@/fav.png"
            class="ml-9"
          ></v-img>
  
          <v-btn text @click="showDialog" class="mr-6 my-text">로그아웃</v-btn>
        </div>
      </v-col>
      

      <v-spacer />

      <template v-slot:extension>
        <v-row>
          <v-spacer />
          <v-divider vertical inset style="height:20px"></v-divider>
          <v-col>
            <v-btn to="/recipe" text style="width: 100%" class="my-text my-vertical-line">레시피 게시판</v-btn>
          </v-col>
          <v-divider vertical inset style="height:20px"></v-divider>
          <v-col>
            <v-btn to="/photo" text style="width: 100%" class="my-text my-vertical-line">요리 사진 게시판</v-btn>
          </v-col>
          <v-divider vertical inset style="height:20px"></v-divider>
          <v-col>
            <v-btn to="/mypage" text style="width: 100%" class="my-text my-vertical-line">마이페이지</v-btn>
          </v-col>
          <v-divider vertical inset style="height:20px"></v-divider>
          <v-spacer />
        </v-row>
      </template>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        headerTitle="로그아웃"
        btnTitle="취소"
        btn2Title="확인"
        @hide="hideDialog"
        @submit="checkDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div>로그아웃 하시겠습니까?</div>
        </template>
      </popup-dialog>
    </v-dialog>
    <!-- 팝업창 형식 -->

  </v-card>
</template>

<style scoped>
.my-text{
  color: #7895B2;
}

.my-vertical-line{
  margin-top: -15px;
  color: #7895B2;
}
</style>

<script>
import router from '@/router/index.js';
import PopupDialog from '@/components/popup.vue';

export default{
  components: {
    PopupDialog
  },
  data(){
    return{
      popupDialog: false,
    }
  },
  methods: {
    showDialog(){ // 팝업창 보이기
      this.popupDialog = true
    },
    hideDialog(){ // 팝업창 숨기기
      this.popupDialog = false
    },
    checkDialog(){ // 팝업창 버튼 클릭시
      // 확인 버튼 클릭시 동작 걸기
      this.logout();
      this.hideDialog();
    },
    logout() {
      localStorage.removeItem("UserInfo");
      router.push({name: 'login'});
    }
  }
}
</script>