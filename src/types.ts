export interface InstagramData {
  profile_user?: Array<{
    string_map_data?: {
      username?: { value: string };
      joined_date?: { value: string };
    };
  }>;
  media_list?: Array<{
    media_type: string;
    timestamp: string;
  }>;
  stories?: any[];
  likes?: any[];
  comments?: any[];
  direct_messages?: Array<{
    participants: string[];
    conversation: Array<{
      sender: string;
      timestamp: string;
    }>;
  }>;
  group_messages?: any[];
  followers?: Array<{
    string_list_data: Array<{
      value: string;
      timestamp: number;
    }>;
  }>;
  following?: Array<{
    string_list_data: Array<{
      value: string;
      timestamp: number;
    }>;
  }>;
}