import type { UserInfo } from './user'

// 考试状态
export type ExamStatus = 'draft' | 'published' | 'upcoming' | 'ongoing' | 'completed' | 'cancelled'

// 考试类型
export type ExamType = 'theory' | 'practice' | 'comprehensive'

// 考试难度
export type ExamDifficulty = 'easy' | 'medium' | 'hard'

// 考试基本信息
export interface Exam {
  id: number
  title: string
  description: string
  type: ExamType
  duration: number // 分钟
  total_score: number
  pass_score: number
  start_date: string
  end_date: string
  status: ExamStatus
  created_by: number
  created_at: string
  updated_at: string
}

// 考试详情
export interface ExamDetail extends Exam {
  sessions: ExamSession[]
  candidates_count: number
  examiners_count: number
  creator: UserInfo
}

// 考试场次
export interface ExamSession {
  id: number
  exam_id: number
  venue_id: number
  start_time: string
  end_time: string
  capacity: number
  enrolled_count: number
  status: ExamStatus
  venue: Venue
  examiners: UserInfo[]
}

// 考场信息
export interface Venue {
  id: number
  name: string
  address: string
  capacity: number
  status: 'active' | 'inactive' | 'maintenance'
  institution_id: number
  created_at: string
  updated_at: string
}

// 考试考生
export interface ExamCandidate {
  id: number
  exam_id: number
  candidate_id: number
  session_id: number | null
  status: 'enrolled' | 'assigned' | 'attended' | 'absent' | 'completed'
  score: number | null
  created_at: string
  updated_at: string
  candidate: UserInfo
  session?: ExamSession
}

// 考试考官
export interface ExamExaminer {
  id: number
  exam_id: number
  examiner_id: number
  session_id: number | null
  role: 'chief' | 'assistant' | 'observer'
  created_at: string
  updated_at: string
  examiner: UserInfo
  session?: ExamSession
}