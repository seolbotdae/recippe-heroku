<template>
  <v-card class="overflow-hidden">
    <v-app-bar
      color="#f5efe6"
      app dense fixed
    >
      <v-spacer />

      <v-toolbar-title>레쉽피</v-toolbar-title>

      <v-spacer />
      <v-spacer />
      <v-spacer />
      <v-spacer />

      <v-btn @click="showDialog">로그아웃</v-btn>

      <v-spacer />

      <template v-slot:extension>
        <v-row>
          <v-spacer />
          <v-col>
            <v-btn to="/recipe" style="width: 100%">레시피 게시판</v-btn>
          </v-col>
          <v-col>
            <v-btn to="/photo" style="width: 100%">요리 사진 게시판</v-btn>
          </v-col>
          <v-col>
            <v-btn to="/mypage" style="width: 100%">마이페이지</v-btn>
          </v-col>
          <v-spacer />
        </v-row>
      </template>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>

    <v-footer
    color="#f5efe6"
    app
    >
      <div>푸터 위치입니다아</div>
    </v-footer>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        headerTitle = "로그아웃"
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