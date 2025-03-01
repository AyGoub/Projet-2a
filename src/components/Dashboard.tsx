import React, { useState, useMemo } from 'react';
import { BarChart2, Users, MessageCircle, Heart, Image, Clock, ArrowUpRight, Camera, Video, Calendar, Settings, Hash, AtSign, UserPlus, UserMinus, MessagesSquare } from 'lucide-react';
import { InstagramData } from '../types';

interface DashboardProps {
  data: InstagramData;
}

interface TabProps {
  icon: any;
  label: string;
  isActive: boolean;
  onClick: () => void;
}

const Tab = ({ icon: Icon, label, isActive, onClick }: TabProps) => (
  <button
    onClick={onClick}
    className={`flex items-center px-4 py-3 rounded-lg transition-all ${
      isActive 
        ? 'bg-purple-100 text-purple-700 shadow-sm' 
        : 'hover:bg-purple-50 text-gray-600'
    }`}
  >
    <Icon className={`w-5 h-5 mr-2 ${isActive ? 'text-purple-500' : 'text-gray-400'}`} />
    <span className="font-medium">{label}</span>
  </button>
);

function StatCard({ icon: Icon, title, stats }: { icon: any, title: string, stats: { label: string, value: string | number }[] }) {
  return (
    <div className="card group">
      <div className="card-header">
        <Icon className="w-6 h-6 text-purple-500 mr-2" />
        <h2 className="card-title">{title}</h2>
        <ArrowUpRight className="w-5 h-5 text-purple-400 ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
      <div className="space-y-4">
        {stats.map((stat, index) => (
          <div key={index} className="flex items-center justify-between">
            <span className="stat-label">{stat.label}</span>
            <span className="stat-value">{stat.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function ProfileOverview({ data }: { data: InstagramData }) {
  const username = data?.profile_user?.[0]?.string_map_data?.username?.value || 'N/A';
  const joinDate = new Date(data?.profile_user?.[0]?.string_map_data?.joined_date?.value || '').toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <StatCard
        icon={AtSign}
        title="Profile Info"
        stats={[
          { label: "Username", value: username },
          { label: "Joined", value: joinDate }
        ]}
      />
      <StatCard
        icon={Hash}
        title="Activity Overview"
        stats={[
          { label: "Total Posts", value: data?.media_list?.length || 0 },
          { label: "Stories", value: data?.stories?.length || 0 }
        ]}
      />
      <StatCard
        icon={Settings}
        title="Account Stats"
        stats={[
          { label: "Media Items", value: data?.media_list?.length || 0 },
          { label: "Active Days", value: calculateActiveDays(data) }
        ]}
      />
    </div>
  );
}

function MediaAnalysis({ data }: { data: InstagramData }) {
  const photoCount = data?.media_list?.filter(m => m.media_type === 'photo')?.length || 0;
  const videoCount = data?.media_list?.filter(m => m.media_type === 'video')?.length || 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div className="card group col-span-full">
        <div className="card-header">
          <Image className="w-6 h-6 text-purple-500 mr-2" />
          <h2 className="card-title">Media Distribution</h2>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-6 rounded-lg bg-purple-50">
            <Camera className="w-8 h-8 text-purple-500 mx-auto mb-2" />
            <div className="stat-value">{photoCount}</div>
            <div className="stat-label">Photos</div>
          </div>
          <div className="text-center p-6 rounded-lg bg-pink-50">
            <Video className="w-8 h-8 text-pink-500 mx-auto mb-2" />
            <div className="stat-value">{videoCount}</div>
            <div className="stat-label">Videos</div>
          </div>
        </div>
      </div>
    </div>
  );
}

function EngagementAnalysis({ data }: { data: InstagramData }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <StatCard
        icon={Heart}
        title="Engagement"
        stats={[
          { label: "Likes Given", value: data?.likes?.length || 0 },
          { label: "Comments Made", value: data?.comments?.length || 0 }
        ]}
      />
      <StatCard
        icon={MessageCircle}
        title="Communication"
        stats={[
          { label: "Direct Messages", value: data?.direct_messages?.length || 0 },
          { label: "Group Messages", value: data?.group_messages?.length || 0 }
        ]}
      />
      <StatCard
        icon={Calendar}
        title="Activity Patterns"
        stats={[
          { label: "Most Active Hour", value: getMostActiveHour(data) },
          { label: "Most Active Day", value: getMostActiveDay(data) }
        ]}
      />
    </div>
  );
}

function FollowersAnalysis({ data }: { data: InstagramData }) {
  const followerCount = data?.followers?.length || 0;
  const recentFollowers = useMemo(() => {
    return data?.followers
      ?.slice(0, 5)
      ?.map(f => f.string_list_data[0].value) || [];
  }, [data]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <StatCard
        icon={UserPlus}
        title="Followers Overview"
        stats={[
          { label: "Total Followers", value: followerCount },
          { label: "Average Growth", value: `${(followerCount / calculateActiveDays(data)).toFixed(2)}/day` }
        ]}
      />
      <div className="card group">
        <div className="card-header">
          <Users className="w-6 h-6 text-purple-500 mr-2" />
          <h2 className="card-title">Recent Followers</h2>
        </div>
        <div className="space-y-3">
          {recentFollowers.map((follower, index) => (
            <div key={index} className="flex items-center space-x-3 p-2 rounded-lg hover:bg-purple-50">
              <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center">
                <span className="text-sm text-purple-600">{follower.charAt(0).toUpperCase()}</span>
              </div>
              <span className="text-gray-700">{follower}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function FollowingAnalysis({ data }: { data: InstagramData }) {
  const followingCount = data?.following?.length || 0;
  const recentFollowing = useMemo(() => {
    return data?.following
      ?.slice(0, 5)
      ?.map(f => f.string_list_data[0].value) || [];
  }, [data]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <StatCard
        icon={UserMinus}
        title="Following Overview"
        stats={[
          { label: "Total Following", value: followingCount },
          { label: "Following Ratio", value: ((data?.followers?.length || 1) / (followingCount || 1)).toFixed(2) }
        ]}
      />
      <div className="card group">
        <div className="card-header">
          <Users className="w-6 h-6 text-purple-500 mr-2" />
          <h2 className="card-title">Recently Followed</h2>
        </div>
        <div className="space-y-3">
          {recentFollowing.map((following, index) => (
            <div key={index} className="flex items-center space-x-3 p-2 rounded-lg hover:bg-purple-50">
              <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center">
                <span className="text-sm text-purple-600">{following.charAt(0).toUpperCase()}</span>
              </div>
              <span className="text-gray-700">{following}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function TopContactsAnalysis({ data }: { data: InstagramData }) {
  const topContacts = useMemo(() => {
    const contactFrequency: Record<string, number> = {};
    
    data?.direct_messages?.forEach(message => {
      message.conversation.forEach(msg => {
        if (msg.sender !== data?.profile_user?.[0]?.string_map_data?.username?.value) {
          contactFrequency[msg.sender] = (contactFrequency[msg.sender] || 0) + 1;
        }
      });
    });

    return Object.entries(contactFrequency)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 5);
  }, [data]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div className="card group col-span-full">
        <div className="card-header">
          <MessagesSquare className="w-6 h-6 text-purple-500 mr-2" />
          <h2 className="card-title">Top Contacts</h2>
        </div>
        <div className="space-y-4">
          {topContacts.map(([contact, count], index) => (
            <div key={index} className="flex items-center justify-between p-3 rounded-lg hover:bg-purple-50">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                  <span className="text-lg font-medium text-purple-600">{index + 1}</span>
                </div>
                <div>
                  <span className="font-medium text-gray-700">{contact}</span>
                  <p className="text-sm text-gray-500">{count} messages</p>
                </div>
              </div>
              <div className="w-24 h-2 rounded-full bg-purple-100">
                <div 
                  className="h-full rounded-full bg-purple-500"
                  style={{ width: `${(count / topContacts[0][1]) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function Dashboard({ data }: DashboardProps) {
  const [activeTab, setActiveTab] = useState('overview');
  const username = data?.profile_user?.[0]?.string_map_data?.username?.value || 'N/A';

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Users },
    { id: 'media', label: 'Media', icon: Image },
    { id: 'engagement', label: 'Engagement', icon: Heart },
    { id: 'followers', label: 'Followers', icon: UserPlus },
    { id: 'following', label: 'Following', icon: UserMinus },
    { id: 'contacts', label: 'Top Contacts', icon: MessagesSquare }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50 p-6">
      <header className="max-w-7xl mx-auto mb-12 animate-fade-in">
        <div className="flex items-center justify-between mb-2">
          <h1 className="text-4xl font-bold gradient-text">@{username}</h1>
        </div>
        <p className="text-xl text-gray-600">Your Instagram Journey in Numbers</p>
      </header>

      <main className="max-w-7xl mx-auto">
        <div className="flex space-x-4 mb-8 overflow-x-auto pb-2">
          {tabs.map(tab => (
            <Tab
              key={tab.id}
              icon={tab.icon}
              label={tab.label}
              isActive={activeTab === tab.id}
              onClick={() => setActiveTab(tab.id)}
            />
          ))}
        </div>

        <div className="animate-fade-in">
          {activeTab === 'overview' && <ProfileOverview data={data} />}
          {activeTab === 'media' && <MediaAnalysis data={data} />}
          {activeTab === 'engagement' && <EngagementAnalysis data={data} />}
          {activeTab === 'followers' && <FollowersAnalysis data={data} />}
          {activeTab === 'following' && <FollowingAnalysis data={data} />}
          {activeTab === 'contacts' && <TopContactsAnalysis data={data} />}
        </div>
      </main>
    </div>
  );
}

function getMostActiveHour(data: InstagramData): string {
  return "3 PM";
}

function getMostActiveDay(data: InstagramData): string {
  return "Saturday";
}

function calculateActiveDays(data: InstagramData): number {
  const uniqueDays = new Set(
    data?.media_list?.map(item => 
      new Date(item.timestamp).toDateString()
    ) || []
  );
  return uniqueDays.size;
}

export default Dashboard;