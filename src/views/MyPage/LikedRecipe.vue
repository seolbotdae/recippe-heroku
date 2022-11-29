<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">

        <v-card min-height="calc(100vh - 120px)" color="#f5efe6">
          
          <div class="recipe-top d-flex justify-space-between align-center pa-5">
            <span style="color:#7895B2; font-weight:900; font-size:1.3em;">좋아요 누른 레시피</span>
          </div>

          <v-row v-if="!isExist" justify="center">
            <v-col cols="12">
              <p style="text-align:center; font-size:1.2em;" class="mt-10">
                좋아요 누른 레시피가 없습니다.
              </p>
            </v-col>
          </v-row>

          <div v-if="isExist">
            <!-- 음식 v card -->
            <v-card height="100" class="mx-5 mb-5" v-for="item in recipes" :key="item.post_id" @click="toLookup(item.post_id)">
              <div class="d-flex align-center">
                <!-- 제목을 받아와서 넣으시면 됩니다. -->
                <span class="mx-10 py-3" style="font-size:1.1em; font-weight:600; color:#7895B2">{{item.title}}</span>
                <v-icon color="red" v-if="item.degree_of_spicy>=1">mdi-chili-mild</v-icon>
                <v-icon color="red" v-if="item.degree_of_spicy>=2">mdi-chili-mild</v-icon>
                <v-icon color="red" v-if="item.degree_of_spicy>=3">mdi-chili-mild</v-icon>
                <v-icon color="red" v-if="item.degree_of_spicy>=4">mdi-chili-mild</v-icon>
                <v-icon color="red" v-if="item.degree_of_spicy>=5">mdi-chili-mild</v-icon>
              </div>
              <div style="border: 0.5px solid #7895B2;" class="mx-5"></div>
              <div class="d-flex align-center justify-space-between">
                <div style="color:#7895B2" class="ml-10 py-3">
                  <!-- 날짜를 받아와서 넣으시면 됩니다. -->
                  <span class="mr-3">{{item.upload_time}}</span>
                  <!-- 이름을 받아와서 넣으시면 됩니다 -->
                  <span>{{item.nickname}}</span>
                </div>
                <div class="mr-6">
                  <!-- 좋아요 받아와서 넣으시면 됩니다. -->
                  <v-icon color="red">mdi-thumb-up-outline</v-icon> {{item.like_count}}
                  <!-- 댓글 가져와서 넣으시면 됩니다. -->
                  <v-icon color="blue" class="ml-2">mdi-comment-processing-outline</v-icon> {{item.comment_count}}
                  <!-- 조회수 가져와서 넣으시면 됩니다. -->
                  <v-icon color="green" class="ml-2">mdi-eye-outline</v-icon> {{item.views}}
                </div>
              </div>
            </v-card>
          </div>
          

        </v-card>
      </v-col>
    </v-row>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        :headerTitle=headerTitle
        :btn1Title=btn1Title
        :btn2=btn2
        @hide="hideDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div>{{ content1 }}</div>
        </template>
      </popup-dialog>
    </v-dialog>

  </v-container>
</template>

<style scoped>
.find-cook{
  display: flex;
}
.black-line{
  border: 0.4px solid #7895B2;
}
.category-search-dropdown{
  display: flex;
  justify-content: center;
}
.write-icon{
  position: fixed;
  bottom: 10%;
  right: 5%;
  z-index: 9;
}
.my-text{
  color:#7895B2;
}
</style>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';
import dropdown from 'vue-dropdowns';
import PopupDialog from '@/components/popup.vue';

export default{
  components: {
    PopupDialog,
    'dropdown': dropdown,
  },
  data () {
    return {
    //팝업창
      popupDialog: false,
      headerTitle: "",
      content1: "",
      btn1Title: "확인",
      btn2: false,

    //레시피 정보들
      recipes: [],
      recipeID: null,

      userNN: "",

    //받아온 것이 없는 경우 체크
      isExist: true,
    }
  },
  mounted() {
    let vm = this;
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    vm.userNN = UserInfo.nickname
    herokuAPI.mylikeposts(vm.userNN, 1)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
          console.log("조회 성공");
          for(let i = 0; response.data[i] != null; i++) {
            vm.recipes.push(response.data[i]);
          }
          console.log("reponse 길이: " + response.data.length);
          if(response.data.length == 0){
            vm.isExist = false;
          }
        }
      })
      .catch(function (e) {
        if(e.response.status == 405) {
          console.log("405 DB 오류");
          vm.requestFailPopup();
        } else if(e.response.status == 500) {
          console.log("500 Unknown error");
          vm.requestFailPopup();
        }
      });
  },
  methods: {
  // 팝업창 관련
    showDialog() { // 팝업창 보이기
      this.popupDialog = true;
    },
    hideDialog() { // 팝업창 숨기기
      this.popupDialog = false;
    },
    requestFailPopup() { // 실패
      this.headerTitle = "요청 실패";
      this.content1 = "레시피 게시글을 요청에 실패했습니다.";
      this.showDialog();
    },

  // 클릭한 레시피 게시글 열람 페이지로 이동
    toLookup(recipeID) {
      router.push({
        path: "/mypage/mypagerecipelookup/"+recipeID,
      })
    },
  }
}
</script>