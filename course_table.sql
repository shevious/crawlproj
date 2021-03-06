/* 연계 강좌 테이블*/
CREATE TABLE TBTNS_COURSE_INFO_TRANS
(
  COURSE_ID               VARCHAR2(32 BYTE)     NOT NULL,
  CON_ID                  VARCHAR2(15 BYTE)     NOT NULL,
  INST_ID                 VARCHAR2(16 BYTE),
  TOTAL_CD                VARCHAR2(10 BYTE),
  SIDO_CD                 VARCHAR2(10 BYTE),
  SIGUNGU_CD              VARCHAR2(10 BYTE),
  COURSE_NM               VARCHAR2(500 BYTE),
  COURSE_DESC_URL         VARCHAR2(4000 BYTE),
  COURSE_PTTN_CD          VARCHAR2(2 BYTE),
  EXTRA_CHARGE_CONTENT    VARCHAR2(200 BYTE),
  EDU_CYCLE_CONTENT       VARCHAR2(200 BYTE),
  EDU_QUOTA_CNT           VARCHAR2(200 BYTE),
  COURSE_START_DT         TIMESTAMP(6) WITH LOCAL TIME ZONE,
  COURSE_END_DT           TIMESTAMP(6) WITH LOCAL TIME ZONE,
  RECEIVE_START_DT        TIMESTAMP(6) WITH LOCAL TIME ZONE,
  RECEIVE_END_DT          TIMESTAMP(6) WITH LOCAL TIME ZONE,
  EDU_TM                  VARCHAR2(200 BYTE),
  EDU_LOCATION_DESC       VARCHAR2(4000 BYTE),
  INQUIRY_TEL_NO          VARCHAR2(100 BYTE),
  TEACHER_PERNM           VARCHAR2(200 BYTE),
  INFO_MNG_INST_ID        VARCHAR2(100 BYTE),
  INFO_INP_INST_ID        VARCHAR2(100 BYTE),
  REG_USER_ID             VARCHAR2(20 BYTE),
  REG_DT                  TIMESTAMP(6) WITH LOCAL TIME ZONE,
  UPD_USER_ID             VARCHAR2(20 BYTE),
  UPD_DT                  TIMESTAMP(6) WITH LOCAL TIME ZONE,
  TAG                     VARCHAR2(4000 BYTE),
  JOB_ABILITY_COURSE_YN   VARCHAR2(1 BYTE),
  CB_EVAL_ACCEPT_YN       VARCHAR2(1 BYTE),
  ALL_EVAL_ACCEPT_YN      VARCHAR2(1 BYTE),
  LANG_CD                 VARCHAR2(10 BYTE),
  STUDY_OS_NM             VARCHAR2(200 BYTE),
  STUDY_WEB_BROWSER_NM    VARCHAR2(100 BYTE),
  STUDY_DEVICE_NM         VARCHAR2(100 BYTE),
  VSL_HANDICAP_SUPP_YN    VARCHAR2(1 BYTE),
  HRG_HANDICAP_SUPP_YN    VARCHAR2(1 BYTE),
  COURSE_CLASS1_CD        VARCHAR2(30 BYTE),
  COURSE_CLASS2_CD        VARCHAR2(30 BYTE),
  COURSE_THUMBNAIL_URL    VARCHAR2(4000 BYTE),
  EDU_TARGET_CD           VARCHAR2(200 BYTE),
  ENROLL_APPL_METHOD_CD   VARCHAR2(50 BYTE),
  EDU_METHOD_CD           VARCHAR2(10 BYTE),
  EDU_LVLDFF_TYPE_CD      VARCHAR2(10 BYTE),
  REF_BOOK_NM             VARCHAR2(200 BYTE),
  SOURCE_DESC             VARCHAR2(4000 BYTE),
  LINK_URL                VARCHAR2(4000 BYTE),
  DEL_YN                  VARCHAR2(1 BYTE),
  COURSE_URL              VARCHAR2(4000 BYTE),
  COURSE_URL_CALL_METHOD  VARCHAR2(10 BYTE),
  MOBILE_URL              VARCHAR2(4000 BYTE),
  MOBILE_URL_CALL_METHOD  VARCHAR2(10 BYTE),
  COURSE_DESC             CLOB,
  ENROLL_AMT              VARCHAR2(200 BYTE)
)
LOB (COURSE_DESC) STORE AS (
  ENABLE      STORAGE IN ROW
  CHUNK       8192
  RETENTION
  NOCACHE
  LOGGING
      STORAGE    (
                  INITIAL          64K
                  NEXT             1M
                  MINEXTENTS       1
                  MAXEXTENTS       UNLIMITED
                  PCTINCREASE      0
                  BUFFER_POOL      DEFAULT
                  FLASH_CACHE      DEFAULT
                  CELL_FLASH_CACHE DEFAULT
                 ))
RESULT_CACHE (MODE DEFAULT)
PCTUSED    0
PCTFREE    10
INITRANS   1
MAXTRANS   255
STORAGE    (
            INITIAL          39M
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
LOGGING 
NOCOMPRESS 
NOCACHE
NOPARALLEL
MONITORING;

COMMENT ON TABLE TBTNS_COURSE_INFO_TRANS IS '연계강좌정보전송';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_ID IS '강좌아이디';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.CON_ID IS '연계아이디';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.INST_ID IS '기관아이디';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.TOTAL_CD IS '토탈코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.SIDO_CD IS '시도코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.SIGUNGU_CD IS '시군구코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_NM IS '강좌명';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_DESC_URL IS '강좌설명URL';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_PTTN_CD IS '강좌유형코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.EXTRA_CHARGE_CONTENT IS '부대비용내용';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.EDU_CYCLE_CONTENT IS '교육주기내용';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.EDU_QUOTA_CNT IS '교육인원수';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_START_DT IS '강좌시작일시';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_END_DT IS '강좌종료일시';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.RECEIVE_START_DT IS '접수시작일시';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.RECEIVE_END_DT IS '접수종료일시';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.EDU_TM IS '교육시간설명';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.EDU_LOCATION_DESC IS '교육장소설명';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.INQUIRY_TEL_NO IS '문의전화번호';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.TEACHER_PERNM IS '강사설명';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.INFO_MNG_INST_ID IS '정보관리기관아이디';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.INFO_INP_INST_ID IS '정보입력기관아이디';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.REG_USER_ID IS '등록회원아이디';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.REG_DT IS '등록일시';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.UPD_USER_ID IS '수정자아이디';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.UPD_DT IS '수정일시';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.TAG IS '태그';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.JOB_ABILITY_COURSE_YN IS '직업능력강좌여부';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.CB_EVAL_ACCEPT_YN IS '학점은행제평가인정여부';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.ALL_EVAL_ACCEPT_YN IS '평생학습계좌제평가인정여부';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.LANG_CD IS '언어코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.STUDY_OS_NM IS '학습운영제제명';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.STUDY_WEB_BROWSER_NM IS '학습웹브라우저명';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.STUDY_DEVICE_NM IS '학습장치명';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.VSL_HANDICAP_SUPP_YN IS '시각장애지원여부';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.HRG_HANDICAP_SUPP_YN IS '청각장애지원여부';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_CLASS1_CD IS '강좌분류1코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_CLASS2_CD IS '강좌분류2코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_THUMBNAIL_URL IS '강좌썸네일URL';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.EDU_TARGET_CD IS '교육대상코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.ENROLL_APPL_METHOD_CD IS '수강신청방법코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.EDU_METHOD_CD IS '교육방법코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.EDU_LVLDFF_TYPE_CD IS '교육난의도구분코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.REF_BOOK_NM IS '참고도서명';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.SOURCE_DESC IS '출처설명';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.LINK_URL IS '링크URL';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.DEL_YN IS '삭제여부';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_URL IS '강좌URL';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_URL_CALL_METHOD IS '강좌URL호출방법코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.MOBILE_URL IS '모바일URL';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.MOBILE_URL_CALL_METHOD IS '모바일URL호출방법코드';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.COURSE_DESC IS '강좌설명';

COMMENT ON COLUMN TBTNS_COURSE_INFO_TRANS.ENROLL_AMT IS '수강금액';



CREATE UNIQUE INDEX PK_TBTNS_COURSE_INFO_TRANS ON TBTNS_COURSE_INFO_TRANS
(CON_ID, COURSE_ID)
LOGGING
PCTFREE    10
INITRANS   2
MAXTRANS   255
STORAGE    (
            INITIAL          3M
            NEXT             1M
            MINEXTENTS       1
            MAXEXTENTS       UNLIMITED
            PCTINCREASE      0
            BUFFER_POOL      DEFAULT
            FLASH_CACHE      DEFAULT
            CELL_FLASH_CACHE DEFAULT
           )
NOPARALLEL;


ALTER TABLE TBTNS_COURSE_INFO_TRANS ADD (
  CONSTRAINT TBTNS_COURSE_INFO_TRANS_PK
  PRIMARY KEY
  (CON_ID, COURSE_ID)
  USING INDEX PK_TBTNS_COURSE_INFO_TRANS
  ENABLE VALIDATE);
