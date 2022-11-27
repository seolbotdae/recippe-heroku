<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <!-- 가장 바깥쪽 카드 -->
        <v-card min-height="1000" color="#f5efe6">
          <div class="d-flex justify-space-between align-end">
            <!-- 뒤로 돌아가기 버튼 -->
            <v-btn text to="/recipe" class="ml-5 mt-5"> - 레시피 게시판</v-btn>
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
              <span class="my-text ml-16 pa-4">{{ requestRecipe.title }}</span>
            </div>
            
            <div class="line mx-5"></div>

            <!-- 요리 타입 변수로 바꿔주세요. -->
            <div class="px-10 d-flex align-center">
              <span class="my-text ml-11 mr-16 pa-4">레시피 종류</span>
              <v-divider vertical></v-divider>
              <span class="my-text ml-16 pa-4">{{ requestRecipe.category }}</span>
              
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
                <v-btn color="#AEBDCA" @click="remainAmmounts" small class="ml-10" width="110" v-if="canDecrease==true">
                  재료 계산
                </v-btn>
              </div>
              
              <v-divider vertical class="mr-1"></v-divider>
              <div class=ma-3>
                <!-- 재료 나타날 v-for -->
                <!-- 재료를 바꾸시면 됩니다. -->
			          <span v-for="item in requestRecipe.Recipe_Ingredients" :key="item.id">
			          	<span v-if="!UnExistIngre.includes(item.id)" style="vertical-align: text-top" class="my-text ml-16">{{item.name}} {{item.amount}}{{item.unit}}</span>
                  <span v-if="UnExistIngre.includes(item.id)" style="vertical-align: text-top" class="my-text-x ml-16">{{item.name}} {{item.amount}}{{item.unit}}</span>
                  <br/>
                  
			          </span>
              </div>       
            </div>
            
            <div class="line mx-5"></div>
          </div>

          <!-- 레시피 내용 입력란 -->
          <!-- 여기 레시피 내용을 바꾸시면 됩니다. -->
          <v-card min-height="100" class="mx-5 mt-5">
            <v-card-title primary-title>
              레시피 내용
            </v-card-title>
            <v-card-text>
              {{ requestRecipe.description }}
            </v-card-text>
          </v-card>

          <!-- 좋아요 숫자 바꿔주세요 -->
          <div class="d-flex justify-center my-5"  :class="{ 'liked' : isLikedAfter == true, 'unliked' : isLikedAfter == false }">
            <v-btn @click="likePhoto" text icon x-large>
              <v-icon>mdi-thumb-up-outline</v-icon>
              {{ requestRecipe.like_count }}
            </v-btn>
          </div>

          <!-- 댓글 개수 바꿔주세요 -->
          <div class="my-text ml-7">댓글 {{requestRecipe.comment_count}}개</div>
          <div class="mx-5 line"></div>
          
          <!-- 댓글 v-for 부분입니다. -->
          <div v-for="item in requestRecipe.comments" :key="item.comment_id">
            <div class="d-flex align-top justify-space-between">
              
              <!-- 사용자 정보 부분입니다 -->
              <div class="d-flex align-top jusify-left">
                <div class="mx-7 my-3 my-comment-commenter">
                  <h3 class="my-text">{{ item.nickname }}</h3>
                  <p class="ma-0 my-text">{{ item.comment_time }}</p>
                </div>
  
              <!-- 댓글 부분 댓글 내용부분입니다. -->
                <div class="my-comment my-text ma-3">
                  {{ item.comments }}
                </div>
              </div>
              
              <!-- 작성자일 경우 주의 버튼 삭제, 연필과 쓰레기통만 뜨게 해주세요. 밑에 있으니 바꿔보세요.-->
              <div class="d-flex my-3 mr-7">
                <div>

                  <v-btn @click="reportComment(item.comment_id)" text icon small v-if="userNN != item.nickname">
                    <v-icon>mdi-alert-outline</v-icon>
                  </v-btn>
                  
                  <div v-if="userNN == item.nickname">
                    <v-btn @click="editComment(item.comment_id)" text icon small color="blue">
                      <v-icon>mdi-pencil-outline</v-icon>
                    </v-btn>
                    <v-btn @click="deleteComment(item.comment_id)" text icon small color="red">
                      <v-icon>mdi-trash-can-outline</v-icon>
                    </v-btn>
                  </div>
                  
                </div>
              </div>
  
            </div>
            <div class="mx-5 line"></div>  
          </div>

          <!-- 댓글 등록 부분입니다. -->
          <div class="d-flex align-top jusify-left my-comment-write">
            <div class="mx-7 my-3 my-comment-commenter ">
              <v-btn @click="addComment" color="#AEBDCA">등록</v-btn>
            </div>

          <!-- 댓글 등록 댓글 내용부분입니다. -->
            <v-card width="100%" color="#f5efe6" flat class="mb-0 mr-5 ml-11" >
              <div class="my-text mb-0 ma-3">
                <v-form ref="form" lazy-validation>
                  <v-textarea
                    outlined
                    background-color="white"
                    label="댓글을 입력해 주세요."
                    v-model="newComment"
                    :rules="newComment_rule"
                    class="mb-0"
                  ></v-textarea>
                </v-form>
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
        :btn2Title=btn2Title
        :btn2=btn2
        @hide="hideDialog"
        @submit="checkDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div>{{ content1 }}<br>{{ content2 }}</div>
        </template>
      </popup-dialog>
    </v-dialog>

    <!-- 쪽지 작성 팝업창 -->
    <v-dialog
      max-width="500"
      v-model="createMailDialog"
    >
      <create-mail-dialog
        :receiverFixed="true"
        :receiver=requestRecipe.nickname
        @hide="hideMailCreate"
      />
    </v-dialog>

    <!-- 신고 팝업창 형식 -->
    <v-dialog
      max-width="400"
      v-model="reportDialog"
    >
      <report-dialog
        :postType=reportType
        :postID=reportID
        @hide="hideReportDialog"
      />
    </v-dialog>

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
.my-text-x{
  color: #f00;
}
.my-comment-commenter{
  width: 200px;
}
.my-comment{
  max-width:500px;
}
.liked {
  color: #f00;
}
.unliked {
  color: #808080;
}


</style>

<script>
import herokuAPI from '@/api/heroku.js';
import dropdown from 'vue-dropdowns';
import PopupDialog from '@/components/popup.vue';
import ReportDialog from '@/components/report.vue';
import CreateMailDialog from '@/components/createMail.vue';

export default{
  components: {
    PopupDialog,
    ReportDialog,
    CreateMailDialog
  },
  data () {
    return {
    // 팝업창
      popupDialog: false,
      reportDialog: false,
      createMailDialog: false,
      headerTitle: "",
      content1: "",
      content2: "",
      btn1Title: "",
      btn2Title: "",
      btn2: false,
      reportType: 0,
      reportID: 0,

      requestRecipe: [],
      UnExistIngre: [],
      newComment: "",
      newComment_rule: [
        v => !!v || '댓글 내용을 입력하세요.',
      ],
      isLikedBefore: null,
      isLikedAfter: null,
      isMine: null,
      deletePost: false,

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
      canDecrease:false,
      userNN: ""
    }
  },
  components: {
    'dropdown': dropdown,
  },
  mounted() {
    let pid = this.$route.params.id;
    console.log("post_id", pid);
    if(pid == null) {
      console.log("ERROR");
    }
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    let vm = this;
    vm.userNN = UserInfo.nickname;
    
  // 레시피 정보 요청
    herokuAPI.recipeLookup(pid, vm.userNN)
      .then(function(response) {
        console.log("게시글 응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            vm.requestRecipe = response.data.recipeInfo;
            vm.isLikedBefore = response.data.likeInfo;
            vm.isLikedAfter = vm.isLikedBefore;
            vm.hotLevel = vm.requestRecipe['degree_of_spicy']
            if(vm.requestRecipe.nickname == vm.userNN) {
              vm.isMine = true;
            } else {
              vm.isMine = false;
            }
          }
      })
      .catch(function (e) {
        if(e.response.status == 500) {
          console.log("500 DB 오류");
          vm.requestFailPopup();
        } else if(e.response.status == 502) {
          console.log("502 Unknown error");
          vm.requestFailPopup();
        }
      });

  // 미보유 재료 요청
    herokuAPI.unExistIngredients(vm.userNN, pid)
      .then(function (response) {
        console.log("test",response.data);
        console.log("test",response.data.length);
        if(response.status == 200) {
          console.log("없는 식재료 가져오기 성공")
          for(let i = 0; i<response.data.length; i++) {
            vm.UnExistIngre.push(response.data[i].id);
          }
          if(response.data.length == 0) vm.canDecrease = true;
          else vm.canDecrease = false;
        }
      })
      .catch(function (e) {
        if(e.response.status == 500) {
          console.log("500 DB 오류");
          vm.ingreFailPopup();
        } else if(e.response.status == 502) {
          console.log("502 Unknown error");
          vm.ingreFailPopup();
        }
      });
  },
  beforeDestroy() {
    let vm = this;
    if (vm.deletePost) return;
    if (vm.isLikedBefore == vm.isLikedAfter) return; // 좋아요 상태 같은 경우
    let task = "";
    if(vm.isLikedBefore) task = "취소"; // 좋아요 취소
    else task = "등록"; // 좋아요 등록

    console.log(task);
    const likeInfo = JSON.stringify({
      "like_id": 0,
      "nickname": vm.userNN,
      "postType": 1,
      "postId": vm.requestRecipe.post_id,
      "task": task
    });
    herokuAPI.recipeLike(likeInfo)
      .then(function (response) {
        if(response.status == 200) console.log("좋아요 " + task + " 성공");
      })
      .catch(function (e) {
        if(e.response.status == 500) {
          console.log("500 취소 오류");
          vm.likeFailPopup(task);
        } else if(e.response.status == 501) {
          console.log("501 등록 오류");
          vm.likeFailPopup(task);
        } else if(e.response.status == 502) {
          console.log("502 Unknown error");
          vm.likeFailPopup(task);
        }
      });
  },
  methods: {
    showDialog() { // 팝업창 보이기
      this.popupDialog = true;
    },
    hideDialog() { // 팝업창 숨기기
      this.popupDialog = false;
    },
    deletePopup() {
      this.headerTitle = "레시피 게시글 삭제";
      this.content1 = "삭제하시겠습니까?";
      this.btn1Title = "취소";
      this.btn2Title = "삭제";
      this.btn2 = true;
      this.showDialog();
    },
    deleteFailPopup() {
      this.headerTitle = "레시피 게시글 삭제 실패";
      this.content1 = "게시글 삭제에 실패했습니다.";
      this.btn1Title = "확인";
      this.btn2 = false;
      this.showDialog();
    },
    requestFailPopup() {
      this.headerTitle = "게시글 불러오기 실패";
      this.content1 = "레시피 게시글을 불러오는데";
      this.content2 = "실패했습니다.";
      this.btn1Title = "확인";
      this.btn2 = false;
      this.showDialog();
    },
    ingreFailPopup() {
      this.headerTitle = "사용자 재료 정보 요청 실패";
      this.content1 = "재료 정보 요청에 실패했습니다";
      this.content2 = "";
      this.btn1Title = "확인";
      this.btn2 = false;
      this.showDialog();
    },
    likeFailPopup(text) {
      this.headerTitle = "좋아요 "+text+" 실패";
      this.content1 = "좋아요 "+text+"에 실패했습니다.";
      this.btn1Title = "취소";
      this.btn2Title = "삭제";
      this.btn2 = true;
      this.showDialog();
    },
    checkDialog() { // 팝업창 버튼 클릭시
      // 확인 버튼 클릭시 동작 걸기
      this.deleteRecipe();
      this.hideDialog();
    },
    deleteRecipe() { // 게시글 삭제
      let vm = this;
      vm.deletePost = true;
      const deleteTarget = JSON.stringify({ requestRecipe });
      herokuAPI.recipeDelete(deleteTarget)
        .then(function (response){
          if(response.status == 200) {
            console.log("삭제 성공");
            router.push({name: 'recipe'});
          }
        })
        .catch(function (e) {
          if(e.response.status == 500) {
            console.log("500 DB 오류");
            vm.deleteFailPopup();
          } else if(e.response.status == 502) {
            console.log("502 Unknown error");
            vm.deleteFailPopup();
          }
        });
    },
    
    showReportDialog() { // 신고 팝업창 보이기
      this.reportDialog = true
    },
    hideReportDialog() { // 신고 팝업창 숨기기
      this.reportDialog = false
    },
    reportComment(comment_id) { // 댓글 신고
      let vm = this;
      vm.reportType = -1;
      vm.reportID = comment_id;
      vm.showReportDialog();
    },

    showMailCreate(){ // 쪽지 작성 팝업창 보이기
      this.createMailDialog = true;
    },
    hideMailCreate(){ // 쪽지 작성 팝업창 숨기기
      this.createMailDialog = false;
    },

    likePhoto() { // 좋아요 버튼 클릭시 동작, 서버랑 통신은 화면을 벗어날 때 초기와 다를 경우에만 실시
      this.isLikedAfter = !this.isLikedAfter;
      if(this.isLikedAfter) ++this.requestRecipe.like_count;
      else --this.requestRecipe.like_count;
    },

    unExistIngredients() {
    // 미보유 재료 요청
      herokuAPI.unExistIngredients(vm.userNN, pid)
        .then(function (response) {
          console.log("test",response.data);
          console.log("test",response.data.length);
          if(response.status == 200) {
            console.log("없는 식재료 가져오기 성공")
            for(let i = 0; i<response.data.length; i++) {
              vm.UnExistIngre.push(response.data[i].id);
            }
            if(response.data.length == 0) vm.canDecrease = true;
            else vm.canDecrease = false;
          }
        })
        .catch(function (e) {
          if(e.response.status == 500) {
            console.log("500 DB 오류");
            vm.ingreFailPopup();
          } else if(e.response.status == 502) {
            console.log("502 Unknown error");
            vm.ingreFailPopup();
          }
        });
    },

    remainAmmounts() {
      let vm = this;
      herokuAPI.decreaseAmount(vm.userNN, vm.requestRecipe.post_id)
        .then(function (response) {
          if(response.status == 200) {
            console.log("남은 재료 계산하기 성공");
            vm.unExistIngredients();
          }
        })
    },
    methodToRunOnSelect(payload) {
      this.object = payload;
    },
    addComment() {
      const validate = this.$refs.form.validate();
      if(!validate) return;
      console.log("유효성검사 통과");
      let vm = this;
      const NewComment = JSON.stringify({
        "comment_id" : 0,
	      "comments" : vm.newComment,
	      "comment_time" : 0,
	      "nickname" : vm.userNN,
	      "post_id" : vm.requestRecipe.post_id
      });
      herokuAPI.commentAdd(NewComment)
        .then(function (response) {
          console.log("응답 정보", response);
          if(response.status == 200) {
            console.log("댓글 등록 성공");
          }
        })
    },
    // editComment(comment_id) {
    //   let vm = this;
    //   const EditComment = JSON.stringify({
    //     "comment_id" : comment_id,
	  //     "comments" : "", // v-for 걸려있는 한개만 어케 변수랑 연결하지...?
	  //     "comment_time" : 0,
	  //     "nickname" : vm.userNN,
	  //     "post_id" : vm.requestRecipe.post_id
    //   });
    //   herokuAPI.commentEdit(EditComment)
    //     .then(function (response) {
    //       console.log("응답 정보", response);
    //       if(response.status == 200) {
    //         console.log("댓글 수정 성공");
    //       }
    //     })
    // },
    deleteComment(comment_id) {
      let vm = this;
      const deleteInfo = JSON.stringify({
        "comment_id": comment_id,
        "nickname": vm.userNN
      });
      herokuAPI.commentDelete(deleteInfo)
        .then(function (response) {
          console.log("응답 정보", response);
          if(response.status == 200) {
            console.log("댓글 삭제 성공");
          }
        })
    },
  }
}
</script>