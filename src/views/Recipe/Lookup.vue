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
                <v-btn color="#AEBDCA" small class="ml-10" width="110">
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

          <!-- 레시피 내용 입력란 -->
          <!-- 여기 레시피 내용을 바꾸시면 됩니다. -->
          <v-card min-height="100" class="mx-5 mt-5">
            <v-card-title primary-title>
              레시피 내용
            </v-card-title>
            <v-card-text>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Harum, debitis ipsa incidunt eum dolores qui voluptate labore ipsum reiciendis, a quaerat magnam itaque voluptates aut repellat vel, aliquid provident laudantium!
              Eius molestiae, corrupti, mollitia et saepe neque numquam aperiam sint reprehenderit unde possimus nostrum, cum ducimus adipisci esse aliquam voluptas nobis. Iste quasi, suscipit fugit architecto eaque sapiente odio asperiores.
              Praesentium consectetur repellendus magni perspiciatis nobis facere assumenda nemo temporibus odit quam rerum ducimus, aliquam recusandae eum pariatur adipisci unde, laborum cupiditate veritatis modi quidem! Vitae suscipit quibusdam omnis molestiae?
              Alias quaerat odit placeat atque consectetur nisi. Hic mollitia eaque beatae aut quasi voluptas illo voluptatibus suscipit aperiam deleniti harum exercitationem voluptatum perferendis atque dicta praesentium itaque, quae rerum temporibus!
              Ratione nesciunt perspiciatis quod error dignissimos minus commodi mollitia assumenda esse ducimus dolorum, hic beatae laboriosam nobis culpa? Eos, minima animi. A hic minima dolore iusto dolores molestias ad fugit!
              Distinctio illum esse nesciunt eaque error dolor necessitatibus, quia ipsam. Est animi praesentium temporibus quasi eum, adipisci reprehenderit in assumenda quia doloremque itaque, expedita nam rem amet similique quo ea!
              Commodi neque voluptas nulla nisi asperiores sint sit maxime distinctio doloribus unde! Sapiente impedit odio totam inventore explicabo perferendis sequi quos quo natus exercitationem, nesciunt enim, quas molestiae nostrum earum!
              Adipisci, eaque, incidunt aliquid necessitatibus expedita, itaque aut reiciendis quibusdam odio nostrum quaerat! Placeat magnam suscipit magni ipsam illum voluptas tenetur ratione voluptates molestias ad iste expedita omnis, assumenda mollitia.
            </v-card-text>
          </v-card>

          <!-- 좋아요 숫자 바꿔주세요 -->
          <div class="d-flex justify-center my-5">
            <v-btn text icon x-large color="red">
              <v-icon>mdi-thumb-up-outline</v-icon>
              1.5k
            </v-btn>
          </div>

          <!-- 댓글 개수 바꿔주세요 -->
          <div class="my-text ml-7">댓글 3개</div>
          <div class="mx-5 line"></div>
          
          <!-- 댓글 v-for 부분입니다. -->
          <div v-for="item in 3">
            <div class="d-flex align-top justify-space-between">
              
              <!-- 사용자 정보 부분입니다 -->
              <div class="d-flex align-top jusify-left">
                <div class="mx-7 my-3 my-comment-commenter">
                  <h3 class="my-text">고독한 미식가</h3>
                  <p class="ma-0 my-text">2022/10/28 18:03:12</p>
                </div>
  
              <!-- 댓글 부분 댓글 내용부분입니다. -->
                <div class="my-comment my-text ma-3">
                  음식이 친절하고 사장님이 맛있어요 ^^
                </div>
              </div>
              
              
  
              <!-- is_owner 변수 사용 예시같이 작성자일 경우 주의 버튼 삭제, 연필과 쓰레기통만 뜨게 해주세요. 밑에 있으니 바꿔보세요.-->
              <div class="d-flex my-3 mr-7">
                <div>

                  <v-btn @click="reportComment" text icon small v-if="!is_owner">
                    <v-icon>mdi-alert-outline</v-icon>
                  </v-btn>
                  
                  <div v-if="is_owner">
                    <v-btn @click="editComment" text icon small color="blue">
                      <v-icon>mdi-pencil-outline</v-icon>
                    </v-btn>
                    <v-btn @click="deleteComment" text icon small color="red">
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

          <!-- 댓글 부분 댓글 내용부분입니다. -->
            <v-card width="100%" color="#f5efe6" flat class="mb-0 mr-5 ml-11" >
              <div class="my-text mb-0 ma-3">
                <v-textarea
                  outlined
                  background-color="white"
                  label="댓글을 입력해 주세요."
                  class="mb-0"
                >
                </v-textarea>
              </div>
            </v-card>
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

.my-comment-commenter{
  width: 200px;
}

.my-comment{
  max-width:500px;
}


</style>

<script>
import heroku from '@/api/heroku.js';
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
      is_owner:false,
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
    addComment() {
      const NewComment = JSON.stringify({
        "comment_id" : 0,
	      "comments" : "web test",
	      "comment_time" : 0,
	      "nickname" : "test",
	      "post_id" : 2
      });
      herokuAPI.commentAdd(NewComment)
        .then(function (response) {
          console.log("응답 정보", response);
          if(response.status == 200) {
            console.log("댓글 등록 성공");
          }
        })
    },
    editComment() {
      const EditComment = JSON.stringify({
        "comment_id" : 14,
	      "comments" : "web test edit",
	      "comment_time" : 0,
	      "nickname" : "test",
	      "post_id" : 2
      });
      herokuAPI.commentEdit(EditComment)
        .then(function (response) {
          console.log("응답 정보", response);
          if(response.status == 200) {
            console.log("댓글 수정 성공");
          }
        })
    },
    deleteComment() {
      const deleteInfo = JSON.stringify({
        "comment_id": 14,
        "nickname": "test"
      });
      herokuAPI.commentDelete(deleteInfo)
        .then(function (response) {
          console.log("응답 정보", response);
          if(response.status == 200) {
            console.log("댓글 삭제 성공");
          }
        })
    },
    reportComment() {
      const reportInfo = JSON.stringify({
	      "contents" : "web comment test",
	      "post_type" : -1,
	      "post_id" : 2,
	      "reporter" : "test"
      })
      herokuAPI.commentReport(reportInfo)
        .then(function (response) {
          console.log("응답 정보", response);
          if(response.status == 200) {
            console.log("댓글 신고 성공");
          }
        })
    }
  }
}
</script>