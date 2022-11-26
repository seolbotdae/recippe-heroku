<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <!-- 요리 직접 검색과 카테고리 선택 -->
        <v-card min-height="100" color="#f5efe6" class="mb-3">
          <!-- 요리 검색 윗줄 -->
          <div class="find-cook flex align-end mb-2" v-if="!categoryBoolean">
            <dropdown class="my-dropdown-toggle my-0 ml-5"
              :options="search_standard"
              :selected="search_object" 
              v-on:updateOption="methodToRunOnSelect" 
              :placeholder="'검색 기준'"
              :closeOnOutsideClick="true">
            </dropdown>
            <v-text-field
              label="요리를 검색하세요"
              hide-details="auto"
              class="mx-5"
            ></v-text-field>
            <v-btn class="mx-3" color="#E8DFCA">
              검색
            </v-btn>
          </div>
          <div class="black-line mx-3" v-if="!categoryBoolean"></div>
          <!-- 요리 검색 밑줄 -->
          <div class="category-search-dropdown mt-2 flex-column">
            <v-btn color="#f5efe6" depressed @click="methodToChangeCategoryBoolean" v-if=!categoryBoolean>카테고리 검색</v-btn>
            <v-btn color="#f5efe6" depressed @click="methodToChangeCategoryBoolean" v-if=categoryBoolean>키워드 검색</v-btn>
            <!-- 카테고리 슬라이드 -->
            <v-card fill-height color="#E8DFCA" v-if=categoryBoolean>
              <v-card min-height="100" class="my-5 mx-5">
                <v-card-title primary-title class="my-text ml-5">
                  재료
                </v-card-title>
                <v-radio-group v-model="value" row class="mt-0 ml-10">
                  <v-radio label="육류" value="육류"></v-radio>
                  <v-radio label="어류" value="어류"></v-radio>
                  <v-radio label="채소류" value="채소류"></v-radio>
                  <v-radio label="과일류" value="과일류"></v-radio>
                </v-radio-group>
              </v-card>

              <v-card min-height="100" class="my-5 mx-5">
                <v-card-title primary-title class="my-text ml-5">
                  조리법
                </v-card-title>
                <v-radio-group v-model="value" row class="mt-0 ml-10">
                  <v-radio label="구이" value="구이"></v-radio>
                  <v-radio label="볶음" value="볶음"></v-radio>
                  <v-radio label="조림" value="조림"></v-radio>
                  <v-radio label="튀김" value="튀김"></v-radio>
                </v-radio-group>
              </v-card>

              <v-card min-height="100" class="my-5 mx-5">
                <v-card-title primary-title class="my-text ml-5">
                  매운맛 단계
                </v-card-title>
                <v-radio-group v-model="value" row class="mt-0 ml-10">
                  <v-radio label="1단계" value="1단계"></v-radio>
                  <v-radio label="2단계" value="2단계"></v-radio>
                  <v-radio label="3단계" value="3단계"></v-radio>
                  <v-radio label="4단계" value="4단계"></v-radio>
                  <v-radio label="5단계" value="5단계"></v-radio>
                </v-radio-group>
              </v-card>
              <div class="d-flex justify-end ma-5">
                <v-btn color="#7895B2">검색</v-btn>
              </div>
            </v-card>
          </div>
        </v-card>



        <v-card min-height="1000" color="#f5efe6">
          <!-- 상단 레시피 게시판 글씨랑 정렬기준 드롭다운 -->
          <div class="recipe-top d-flex justify-space-between align-center pa-5">
            <span style="color:#7895B2; font-weight:900; font-size:1.3em;">레시피 게시판</span>
            <!-- 드롭다운으로 대체할 예정 -->
            <dropdown class="my-dropdown-toggle"
              :options="arrayOfObjects" 
              :selected="object" 
              v-on:updateOption="methodToRunOnSelect" 
              :placeholder="'정렬 기준'"
              :closeOnOutsideClick="true">
            </dropdown>
          </div>

          <!-- 글쓰기 버튼 -->
          <v-btn fab to="/recipe/create" x-large color="primary" class="write-icon">
            <v-icon dark>mdi-pencil-outline</v-icon>
          </v-btn>

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



          <!-- 페이지 이동 -->
          <v-pagination v-model="page" length="5" class="pb-10">
          </v-pagination>
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
      total_page: null,

    //드롭다운
      //검색 기준
      search_standard: [
        {name: '요리 이름'},
        {name: '작성자'}
      ],
      search_object: {
        name: '검색 기준',
      },
      //정렬 기준 objects
      arrayOfObjects: [
        { name: '최근 순'},
        { name: '조회 순'},
        { name: '좋아요 순'}
      ],
      object: {
        name: '정렬 기준',
      },

    //카테고리 슬라이드
      categoryBoolean : false,
    }
  },
  components: {
    'dropdown': dropdown,
  },
  mounted() {
    let vm = this;
    herokuAPI.recipeList(1)
      .then(function(response) {
        console.log("리스트 응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            for(let i = 0; response.data.recipeList[i] != null; i++) {
              vm.recipes.push(response.data.recipeList[i]);
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
    searchRequestFailPopup() { // 검색 실패
      this.headerTitle = "요청 실패";
      this.content1 = "검색 결과 요청에 실패했습니다.";
      this.showDialog();
    },
    sortRequestFailPopup() { // 정렬 실패
      this.headerTitle = "요청 실패";
      this.content1 = "정렬 정보 요청에 실패했습니다.";
      this.showDialog();
    },

  // 클릭한 레시피 게시글 열람 페이지로 이동
    toLookup(recipeID) {
      router.push({
        path: "/recipe/lookup/"+recipeID,
      })
    },

    searchRecipeList() {
      let list = [];
      let tp;
      const searchInfo = JSON.stringify({
        "searchType": "카테고리",
        "categories": "test0-test2",
        "keywordType": null,
        "keyword": null,
        "page": 1
      });
      herokuAPI.recipeSearch(searchInfo)
        .then(function(response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
              console.log("검색 성공");
              for(let i = 0; response.data.recipeList[i] != null; i++) {
                list.push(response.data.recipeList[i]);
              }
              tp = response.data.total_page;
            }
        })
        .catch(function (e) {
          if(e.response.status == 500) {
            console.log("500 DB 오류");
            vm.searchRequestFailPopup();
          } else if(e.response.status == 502) {
            console.log("502 Unknown error");
            vm.searchRequestFailPopup();
          }
        });
      this.recipes = list;
      this.total_page = tp;
    },

    sortRecipeList() {
      let list = [];
      const sortInfo = JSON.stringify({
        "arrangeBy": "좋아요 순",
        "page": 1
      });
      herokuAPI.recipeSort(sortInfo)
        .then(function (response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
            console.log("정렬 성공");
            for(let i = 0; response.data[i] != null; i++) {
              list.push(response.data[i]);
            }
          }
        })
        .catch(function (e) {
          if(e.response.status == 500) {
            console.log("500 DB 오류");
            vm.sortRequestFailPopup();
          } else if(e.response.status == 502) {
            console.log("502 Unknown error");
            vm.sortRequestFailPopup();
          }
        });
      this.recipes = list;
    },

    methodToRunOnSelect(payload) {
      this.object = payload;
    },

    // 카테고리 검색 슬라이드 버튼 함수
    methodToChangeCategoryBoolean() {
      if (this.categoryBoolean == true) {
        this.categoryBoolean = false
      } else {
        this.categoryBoolean = true
      }
    },
  }
}
</script>