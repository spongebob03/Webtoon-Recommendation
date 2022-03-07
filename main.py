from data_naver import get_outline, get_detail
from save import save_file

naver_simple = get_outline()
save_file(naver_simple, "n-simple")

naver_detail = get_detail("n-simple.csv")
save_file(naver_detail, "n-detail")