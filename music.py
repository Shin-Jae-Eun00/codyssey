# 1. 단순 연결 리스트
class Node:
    def __init__(self, data):
        self.data = data      # 노드 데이터 (노래 제목 등)
        self.next = None      # 다음 노드를 가리키는 포인터

head = None

posHEAD = 0   # 맨 앞
posTAIL = 1   # 맨 뒤
posNODE = 2   # 특정 노드 뒤

# 삽입 함수
def insert(data, position=posHEAD, node=None):
    global head

    new_node = Node(data)   # 새 노드 생성

    # 1. 리스트가 비어있는 경우
    if head is None:
        head = new_node
        return

    # 2. 맨 앞 삽입
    if position == posHEAD:
        new_node.next = head
        head = new_node
        return

    # 3. 맨 뒤 삽입
    if position == posTAIL:
        current = head
        while current.next:
            current = current.next
        current.next = new_node
        return

    # 4. 특정 노드 뒤 삽입
    if position == posNODE and node is not None:
        current = head
        while current and current.data != node:
            current = current.next

        if current is None:
            print(f"{node} 항목을 찾을 수 없습니다.")
            return

        new_node.next = current.next
        current.next = new_node

# 삭제 함수 (특정 항목 삭제)
def delete(target):
    global head

    if head is None:
        print("리스트가 비어있습니다.")
        return

    # head 삭제
    if head.data == target:
        head = head.next
        print(f"{target} 삭제 완료 (head)")
        return

    current = head
    prev = None

    while current and current.data != target:
        prev = current
        current = current.next

    if current is None:
        print(f"{target} 값을 찾을 수 없습니다.")
        return

    prev.next = current.next
    print(f"{target} 삭제 완료")

# 전체 리스트 반환 (보너스)
def get_list():
    global head

    current = head
    result = []

    while current:
        result.append(current.data)
        current = current.next

    return result

# 2. 원형 연결 리스트
class CNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularList:
    def __init__(self):
        self.head = None
        self.current = None   # 현재 재생 위치

    # 삽입 (맨 끝)
    def insert(self, data):
        new_node = CNode(data)

        # 비어있는 경우
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
            self.current = self.head
            return

        temp = self.head

        # 마지막 노드 찾기
        while temp.next != self.head:
            temp = temp.next

        temp.next = new_node
        new_node.next = self.head

    # 삭제
    def delete(self, target):
        if self.head is None:
            print("리스트 비어있음")
            return

        temp = self.head

        # head 삭제
        if temp.data == target:
            if temp.next == self.head:
                self.head = None
                self.current = None
                return

            last = self.head
            while last.next != self.head:
                last = last.next

            self.head = self.head.next
            last.next = self.head
            return

        prev = temp
        temp = temp.next

        while temp != self.head:
            if temp.data == target:
                prev.next = temp.next
                return
            prev = temp
            temp = temp.next

        print("삭제할 값 없음")

    # 다음 곡 가져오기 (핵심)
    def get_next(self):
        if self.current is None:
            return None

        data = self.current.data
        self.current = self.current.next
        return data

    # 검색
    def search(self, target):
        if self.head is None:
            return False

        temp = self.head

        while True:
            if temp.data == target:
                return True
            temp = temp.next
            if temp == self.head:
                break

        return False

# 3. 음악 플레이어
import pygame
import time
import os


class MusicPlayer:
    def __init__(self, playlist, mode="repeat"):
        self.playlist = playlist
        self.mode = mode   # normal / repeat / single
        pygame.mixer.init()

    def play(self):
        print(f"재생 모드: {self.mode}")

        first_song = None
        loop_check = False

        while True:
            # 모드별 곡 선택
            # single → 현재 곡만 반복
            if self.mode == "single":
                if self.playlist.current is None:
                    print("곡 없음")
                    break
                song = self.playlist.current.data

            else:
                song = self.playlist.get_next()

            if song is None:
                print("곡 없음")
                break

            # normal 모드 → 한 바퀴만 재생
            if self.mode == "normal":
                if first_song is None:
                    first_song = song
                elif song == first_song:
                    if loop_check:
                        print("재생 종료 (normal 모드)")
                        break
                    loop_check = True

            print(f"재생: {song}")

            try:
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()

                # 음악 끝날 때까지 대기
                while pygame.mixer.music.get_busy():
                    time.sleep(1)

            except:
                print(f"파일 오류: {song}")

# 4. 메인 실행
if __name__ == "__main__":
    # 단순 연결 리스트 테스트
    insert("Song A", posHEAD)
    insert("Song B", posTAIL)
    insert("Song C", posTAIL)

    insert("Intro", posHEAD)
    insert("Middle Song", posNODE, "Song A")

    print("현재 리스트:", " → ".join(get_list()))

    delete("Song B")

    print("삭제 후:", " → ".join(get_list()))

    # 원형 리스트 + 음악 플레이어
    circularlist = CircularList()

    music_folder = "music"

    if os.path.exists(music_folder):
        for file in os.listdir(music_folder):
            if file.endswith(".mp3"):
                path = os.path.join(music_folder, file)
                circularlist.insert(path)

        # 플레이어 실행 (모드 선택)
        player = MusicPlayer(circularlist, mode="repeat")
        player.play()

    else:
        print("music 폴더가 없습니다.")