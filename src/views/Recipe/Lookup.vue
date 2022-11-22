<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <!-- 가장 바깥쪽 카드 -->
        <v-card min-height="1000" color="#f5efe6">
          <div class="d-flex justify-space-between align-end">
            <!-- 뒤로 돌아가기 버튼 -->
            <v-btn text to="/photo" class="ml-5 mt-5"> - 레시피 게시판</v-btn>
            <v-btn text class="mr-5">
              <v-icon>mdi-menu</v-icon>
            </v-btn>
          </div>
          
          <!-- 게시글 정보 입력란 -->
          <div class="mt-5">
            <div class="line mx-5"></div>

            <!-- 요리 이름 변수로 바꿔주세요. -->
            <div class="px-10 d-flex align-center">
              <span class="my-text ml-11 mr-16 pa-4">레시피 제목</span>
              <v-divider vertical></v-divider>
              <span class="my-text ml-16 pa-4">김치볶음밥</span>
            </div>
            
            <div class="line mx-5"></div>

            <!-- 요리 타입 변수로 바꿔주세요. -->
            <div class="px-10 d-flex align-center">
              <span class="my-text ml-11 mr-16 pa-4">레시피 종류</span>
              <v-divider vertical></v-divider>
              <span class="my-text ml-16 pa-4">한식</span>
              
            </div>

            <div class="line mx-5"></div>

            <!-- script에 recippeTypeObject 를 바꾸시면 됩니다. -->
            <div class="px-10 d-flex align-center">
              <span class="my-text ml-11 mr-16 pa-4">매운맛 단계</span>
              <v-divider vertical class="mr-3"></v-divider>
              
              <v-icon color="red" v-if="hotLevel>=1" class="ml-16">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="hotLevel>=2">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="hotLevel>=3">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="hotLevel>=4">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="hotLevel>=5">mdi-chili-mild</v-icon>
            </div>

            <div class="line mx-5"></div>

            <div class="px-10 d-flex wrap align-center ingredients" style="position:relative">
              
              <div class="d-flex flex-column">
                <span class="my-text ml-10 mr-16 pa-4">식재료 및 양</span>
                <v-btn color="#AEBDCA" small class="ml-11" width="100">
                  재료 계산
                </v-btn>
              </div>
              
              <v-divider vertical class="mr-1"></v-divider>
              <div class=ma-3>
                <!-- 재료 나타날 v-for -->
                <!-- 재료를 바꾸시면 됩니다. -->
			          <span v-for="item in 10">
			          	<span style="vertical-align: text-top" class="my-text ml-16">고등어 1마리</span>
                  <br/>
                  
			          </span>
              </div>       
            </div>
            
            <div class="line mx-5"></div>
          </div>

          <!-- 레시피 설명 입력란 -->
          <!-- 여기 value를 바꾸시면 됩니다. -->
          <v-textarea
            outlined
            class="mt-5 mx-5"
            name="name"
            label="레시피 설명을 입력하세요"
            placeholder="레시피 설명을 입력하세요"
			      value="고등어 손질하고 재료 다 넣어서 졸이면 됩니다. ^^"
            height="300"
            background-color="white"
          ></v-textarea>

          <div class="d-flex justify-end mr-5 pb-5">
            <v-btn color="#AEBDCA" class="mr-5">등록취소</v-btn>
            <v-btn color="#AEBDCA" class="mr-2">등록하기</v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.line{
  border:1px solid #AEBDCA
}

.ingredients{
  min-height: 300px;
}

.add-ingredient{
  position: absolute;
  bottom: 5%;
  right: 5%;
}

.my-text{
  color: #42688e;
}
</style>

<script>
import herokuAPI from '@/api/heroku.js';
import dropdown from 'vue-dropdowns';

export default {
  data () {
    return {
      requestRecipe: null,
      isLiked: null,
      recippeType: [
        { name: '최근 순'},
        { name: '조회 순'},
        { name: '좋아요 순'}
      ],
      recippeTypeObject: {
        name: '한식',
      },
      hotLevel: [
        { name: '1단계'},
        { name: '2단계'},
        { name: '3단계'},
        { name: '4단계'},
        { name: '5단계'}
      ],
      hotLevelObject: {
        name: '3단계',
      },
      hotLevel:4,
    }
  },
  components: {
    'dropdown': dropdown,
  },
  // mounted() {
  //   let pid = this.$route.params.id;
  //   console.log("post_id", pid);
  //   if(pid == null) {
  //     console.log("ERROR");
  //   }
  //   const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
  //   let vm = this;
  //   herokuAPI.recipeLookup(pid, UserInfo.nickname)
  //     .then(function(response) {
  //       console.log("게시글 응답 온거", response);
  //       if(response.status == 200) {
  //           console.log("조회 성공");
  //           vm.requestRecipe = response.data.recipeInfo;
  //           vm.isLiked = response.data.likeInfo;
  //         }
  //     })
  // },
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
      let vm = this;
      const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
      const likeInfo = JSON.stringify({
        "like_id": 0,
        "nickname": UserInfo.nickname,
        "postType": 1,
        "postId": vm.requestRecipe.post_id,
        "task": task
      });
      console.log(likeInfo)
      if(task == '등록') {
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
    },
    reportRecipe() {
      const reportInfo = JSON.stringify({
        "id": 0,
        "contents": "web test",
        "post_type": 1,
        "post_id": 46,
        "reporter": "test"
      });
      herokuAPI.recipeReport(reportInfo)
        .then(function (response) {
          if(response.status == 200) {
            console.log("게시글 신고 성공");
          }
        })
    },
    lookupUnExistIngredients() {
      herokuAPI.unExistIntredients("test", 43)
        .then(function (response) {
          if(response.status == 200) {
            console.log("없는 식재료 가져오기 성공")
          }
        })
    },
    remainAmmounts() {
      herokuAPI.decreaseAmount("test", 43)
        .then(function (response) {
          if(response.status == 200) {
            console.log("남은 재료 계산하기 성공")
          }
        })
    },
    methodToRunOnSelect(payload) {
      this.object = payload;
    },
  }
}
</script>