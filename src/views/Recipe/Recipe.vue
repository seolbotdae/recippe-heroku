<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <!-- 요리 직접 검색과 카테고리 선택 -->
        <v-card min-height="100" color="#f5efe6" class="mb-3">
          <!-- 요리 검색 윗줄 -->
          <div class="find-cook flex align-end mb-2">
            <dropdown class="my-dropdown-toggle my-0 ml-5"
              :options="search_standard"
              :selected="search_object" 
              v-on:updateOption="searchStandardRunOnSelect" 
              :placeholder="'검색 기준'"
              :closeOnOutsideClick="true">
            </dropdown>
            <v-text-field
              label="요리를 검색하세요"
              v-model="searchText"
              hide-details="auto"
              class="mx-5"
            ></v-text-field>
            <v-btn @click="beforeSelectKeyword" class="mx-3" color="#E8DFCA">
              검색
            </v-btn>
          </div>
          <div class="black-line mx-3"></div>
          <!-- 요리 검색 밑줄 -->
          <div class="category-search-dropdown mt-2 flex-column">
            <v-btn color="#f5efe6" depressed @click="showCategoryDialog">카테고리 검색</v-btn>
          </div>
        </v-card>

        <v-card min-height="calc(100vh - 233px)" color="#f5efe6">
          <!-- 상단 레시피 게시판 글씨랑 정렬기준 드롭다운 -->
          <div class="recipe-top d-flex justify-space-between align-center pa-5">
            <span style="color:#7895B2; font-weight:900; font-size:1.3em;">레시피 게시판</span>
            <!-- 드롭다운으로 대체할 예정 -->
            <dropdown class="my-dropdown-toggle"
              :options="sort_standard" 
              :selected="sort_object" 
              v-on:updateOption="sortStandardRunOnSelect" 
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
          <v-pagination 
            v-model="page" 
            :length="pageLength"
            class="pb-10"
            @input="handlePage"  
          >
          </v-pagination>
        </v-card>
      </v-col>
    </v-row>

    <!-- 카테고리 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="categoryDialog"
    >
      <category-dialog
        @category="beforeSelectCategory"
        @hide="hideCategoryDialog"
      />
    </v-dialog>

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
import CategoryDialog from '@/components/Category.vue'

export default{
  components: {
    PopupDialog,
    'dropdown': dropdown,
    CategoryDialog
  },
  data () {
    return {
    //팝업창
      popupDialog: false,
      headerTitle: "",
      content1: "",
      btn1Title: "확인",
      btn2: false,
      categoryDialog: false,

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
        name: '요리 이름',
      },
      //정렬 기준 objects
      sort_standard: [
        { name: '최근 순'},
        { name: '조회 순'},
        { name: '좋아요 순'}
      ],
      sort_object: {
        name: '최근 순',
      },

      //현재 검색 기준
      currentSearchStandard : "요리 이름",
      searchText: "",
      searchTextStorage: "",
      searchTypeStorage: "",
      category: "",

      currentRequestType : "정렬",

      //페이지네이션 길이
      pageLength : 1,

      //현재 페이지
      page : 1,
    }
  },
  mounted() {
    let vm = this;
    herokuAPI.recipeList(1)
      .then(function(response) {
        console.log("리스트 응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            vm.pageLength = response.data.total_page;
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

    showCategoryDialog() {
      this.categoryDialog = true;
    },
    hideCategoryDialog() {
      this.categoryDialog = false;
    },
    beforeSelectCategory(name) {
      let vm = this;
      vm.currentRequestType = "카테고리";
      vm.category = name;
      vm.selectCategory(name, 1);
    },
    selectCategory(name, page) {
      let vm = this;
      const searchInfo = JSON.stringify({
        "searchType": "카테고리",
        "categories": name,
        "keywordType": null,
        "keyword": null,
        "page": page
      });
      vm.recipes = [];
      herokuAPI.recipeSearch(searchInfo)
        .then(function(response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
              console.log("검색 성공");
              for(let i = 0; response.data.recipeList[i] != null; i++) {
                vm.recipes.push(response.data.recipeList[i]);
              }
              vm.pageLength = response.data.total_page;
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
    },
    beforeSelectKeyword() {
      this.searchTextStorage = this.searchText;
      this.searchTypeStorage = this.search_object.name;
      this.selectKeyword(1);
    },
    selectKeyword(page) {
      let vm = this;
      vm.currentRequestType = "타이핑";
      const searchInfo = JSON.stringify({
        "searchType": "타이핑",
        "categories": null,
        "keywordType": vm.searchTypeStorage,
        "keyword": vm.searchTextStorage,
        "page": page
      });
      vm.recipes = [];
      console.log(searchInfo);
      herokuAPI.recipeSearch(searchInfo)
        .then(function(response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
              console.log("검색 성공");
              for(let i = 0; response.data.recipeList[i] != null; i++) {
                vm.recipes.push(response.data.recipeList[i]);
              }
              vm.pageLength = response.data.total_page;
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
    },

  // 클릭한 레시피 게시글 열람 페이지로 이동
    toLookup(recipeID) {
      router.push({
        path: "/recipe/lookup/"+recipeID,
      })
    },

    sortRecipeList(page, order_by) {
      let vm = this;
      vm.recipes = [];
      vm.currentRequestType = "정렬"
      
      const sortInfo = JSON.stringify({
        "arrangeBy": order_by,
        "page": page
      });
      herokuAPI.recipeSort(sortInfo)
        .then(function (response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
            console.log("정렬 성공");
            for(let i = 0; response.data.recipeList[i] != null; i++) {
              vm.recipes.push(response.data.recipeList[i]);
            }
            window.scrollTo({top:0});
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
    },

    // 검색 드롭다운 선택시 실행되는 함수
    searchStandardRunOnSelect(payload) {
      this.object = payload;
      if (this.object.name == "요리 이름") {
        console.log("요리 이름 선택");
        this.search_object.name = '요리 이름';
        this.currentSearchStandard = '요리 이름';
      }else if(this.object.name == "작성자") {
        console.log("작성자 선택");
        this.search_object.name = '작성자';
        this.currentSearchStandard = '작성자';
      }
    },

    // 정렬 드롭다운 선택시 실행되는 함수
    sortStandardRunOnSelect(payload) {
      this.object = payload;
      if (this.object.name == "최근 순") {
        console.log("최근 순 선택");
        this.sort_object.name = "최근 순";

        this.page = 1;
        console.log(this.page, this.sort_object.name);
        this.sortRecipeList(this.page, this.sort_object.name);

      } else if (this.object.name == "조회 순") {
        console.log("조회 순 선택");
        this.sort_object.name = "조회수 순";

        this.page = 1;
        console.log(this.page, this.sort_object.name);
        this.sortRecipeList(this.page, this.sort_object.name);

      } else if (this.object.name == "좋아요 순") {
        console.log("좋아요 순 선택");
        this.sort_object.name = "좋아요 순";

        this.page = 1;
        console.log(this.page, this.sort_object.name);
        this.sortRecipeList(this.page, this.sort_object.name);

      }
    },

    //페이지네이션 함수
    handlePage(page){
      let vm = this;
      if(vm.currentRequestType == "정렬") vm.sortRecipeList(page, vm.sort_object.name);
      else if (vm.currentRequestType == "카테고리") vm.selectCategory(vm.category, page);
      else if (vm.currentRequestType == "타이핑") vm.selectKeyword(page);
    }
  }
}
</script>